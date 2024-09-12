from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import time
import uuid

from enums.day_of_week_enum import DayOfWeekEnum
from services.service_provider_service import ServiceProviderService
from repositories.service_provider_repository import ServiceProviderRepository
from entities.service_provider_entity import ServiceProviderEntity
from entities.user_provider_association_entity import UserProviderAssociationEntity
from entities.provider_phone_entity import ProviderPhoneEntity
from entities.working_hours_entity import WorkingHoursEntity
from entities.service_provider_location_entity import ServiceProviderLocationEntity
from boundaries.service_provider_create_boundary import ServiceProviderCreateBoundary
from errors.validation_error import ValidationError
from errors.database_error import DatabaseError
from dto.service_provider_dto import ServiceProviderDTO
from dto.open_service_provider_dto import OpenServiceProviderDTO
from utils.location import Location


class ServiceProviderServiceImplementation(ServiceProviderService):
    def __init__(self, repository: ServiceProviderRepository):
        self.repository = repository

    async def create_service_provider(self, boundary: ServiceProviderCreateBoundary,
                                      db: AsyncSession) -> ServiceProviderEntity:
        try:
            # Create the main service provider entity
            service_provider = ServiceProviderEntity(
                provider_id=uuid.uuid4(),
                name=boundary.name,
                service_type=boundary.service_type,
                email=boundary.email,
                membership="Free"  # Default membership to 'Free'
            )

            # Save the service provider entity
            saved_provider = await self.repository.save_service_provider(service_provider, db)

            # Prepare associated entities using list comprehensions
            user_entities = [
                UserProviderAssociationEntity(
                    user_id=user_boundary.user_id,
                    provider_id=saved_provider.provider_id,
                    role=user_boundary.role
                ) for user_boundary in boundary.users
            ]

            phone_entities = [
                ProviderPhoneEntity(
                    phone_id=uuid.uuid4(),
                    provider_id=saved_provider.provider_id,
                    phone_number=phone.phone_number
                ) for phone in boundary.phones
            ]

            working_hours_entities = [
                WorkingHoursEntity(
                    provider_id=saved_provider.provider_id,
                    day_of_week=working_hours.day_of_week,
                    start_time=working_hours.start_time,
                    end_time=working_hours.end_time
                ) for working_hours in boundary.working_hours
            ]

            location_entities = [
                ServiceProviderLocationEntity(
                    provider_id=saved_provider.provider_id,
                    full_address=location.full_address,
                    geo_location=location.geo_location
                ) for location in boundary.locations
            ]

            # Use repository methods to handle bulk insertions
            await self.repository.add_users(user_entities, db)
            await self.repository.add_phones(phone_entities, db)
            await self.repository.add_working_hours(working_hours_entities, db)
            await self.repository.add_locations(location_entities, db)

            # Commit the transaction
            await db.commit()
            return saved_provider

        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "unique constraint" in error_message:
                raise ValidationError(
                    "A service provider with similar details already exists, violating a unique constraint."
                )
            elif "foreign key constraint" in error_message:
                raise ValidationError("One or more foreign key references (e.g., users, phones) are invalid.")
            else:
                raise DatabaseError(f"Service provider creation failed due to a database constraint: {error_message}")

        except SQLAlchemyError:
            await db.rollback()
            raise DatabaseError("An unexpected database error occurred while creating the service provider.")

    async def update_service_provider(self, provider_id: uuid.UUID, name: Optional[str], service_type: Optional[str],
                                      email: Optional[str], db: AsyncSession) -> ServiceProviderEntity:
        provider = await self.repository.get_by_id(provider_id, db)
        if not provider:
            raise ValidationError(f"Service provider with ID '{provider_id}' was not found.")

        # Track if any data was actually updated
        has_updates = False

        # Check if the fields are provided and not None, and apply updates if there are new values
        if name is not None and name != provider.name:
            provider.name = name
            has_updates = True
        if service_type is not None and service_type != provider.service_type:
            provider.service_type = service_type
            has_updates = True
        if email is not None and email != provider.email:
            provider.email = email
            has_updates = True

        # If there are no changes, skip the update
        if not has_updates:
            return provider  # Return the current state without updating the database

        try:
            updated_provider = await self.repository.update_service_provider(provider, db)
            await db.commit()
            return updated_provider

        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "unique constraint" in error_message:
                raise ValidationError("Updating this service provider violates a unique constraint.")
            else:
                raise DatabaseError(f"Service provider update failed due to a database constraint: {error_message}")

        except SQLAlchemyError:
            await db.rollback()
            raise DatabaseError("An unexpected database error occurred while updating the service provider.")

    async def get_service_providers(self, provider_id: Optional[uuid.UUID], user_id: Optional[uuid.UUID], service_type: Optional[str],
                                    name: Optional[str], phone_number: Optional[str], day_of_week: Optional[str],
                                    desired_time: Optional[time], membership: Optional[str],
                                    longitude: Optional[float], latitude: Optional[float], radius_km: Optional[float],
                                    page: int, size: int, db: AsyncSession) -> List[ServiceProviderDTO]:
        try:
            day_of_week_enum = None  # Initialize day_of_week_enum to None

            # Validate day_of_week if provided
            if day_of_week:
                try:
                    day_of_week_enum = DayOfWeekEnum[day_of_week.upper()]  # Validate against Enum
                except KeyError:
                    raise ValidationError(f"Invalid day of the week: {day_of_week}")

            # Fetch providers from the repository
            providers = await self.repository.get_service_providers(
                provider_id=provider_id,
                user_id=user_id,
                service_type=service_type,
                name=name,
                phone_number=phone_number,
                day_of_week=day_of_week_enum if day_of_week else None,
                desired_time=desired_time,
                membership=membership,
                longitude=longitude,
                latitude=latitude,
                radius_km=radius_km,
                page=page,
                size=size,
                db=db
            )

            return providers

        except Exception as e:
            raise DatabaseError(f"An error occurred while fetching service providers: {str(e)}")

    async def get_open_service_providers(self, day_of_week: str, desired_time: time, page: int, size: int,
                                         db: AsyncSession) -> List[OpenServiceProviderDTO]:
        try:
            # Validate the incoming day_of_week
            try:
                day_of_week_enum = DayOfWeekEnum[day_of_week.upper()]  # Match against Enum
            except KeyError:
                raise ValidationError(f"Invalid day of the week: {day_of_week}")

            open_providers = await self.repository.get_open_service_providers(
                day_of_week_enum, desired_time, page, size, db
            )

            # Convert to DTOs with Location transformation
            for provider in open_providers:
                for loc in provider.locations:
                    loc.geo_location = Location(latitude=loc.geo_location.latitude, longitude=loc.geo_location.longitude)
            return open_providers

        except SQLAlchemyError as e:
            raise DatabaseError(f"An error occurred while fetching open service providers: {str(e)}")
