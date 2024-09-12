from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
import uuid

from boundaries.service_provider_location_boundary import ServiceProviderLocationBoundary
from entities.service_provider_location_entity import ServiceProviderLocationEntity
from repositories.service_provider_location_repository import ServiceProviderLocationRepository
from boundaries.service_provider_location_create_boundary import ServiceProviderLocationCreateBoundary
from errors.database_error import DatabaseError
from errors.validation_error import ValidationError
from services.service_provider_location_service import ServiceProviderLocationService
from utils.location import Location
from geoalchemy2.elements import WKBElement
from shapely import wkb

class ServiceProviderLocationServiceImplementation(ServiceProviderLocationService):

    def __init__(self, repository: ServiceProviderLocationRepository):
        self.repository = repository

    async def add_location(self, location_boundary: ServiceProviderLocationCreateBoundary, db: AsyncSession) -> ServiceProviderLocationEntity:
        location = ServiceProviderLocationEntity(
            provider_id=location_boundary.provider_id,
            full_address=location_boundary.location.full_address,
            geo_location=location_boundary.location.geo_location  # Storing as PostGIS point
        )
        try:
            saved_location = await self.repository.add_location(location, db)
            await db.commit()

            # Convert geo_point to Location object before returning
            saved_location.geo_location = await self._convert_geo_point(saved_location.geo_location)
            return saved_location
        except IntegrityError as e:
            await db.rollback()
            raise ValidationError(f"Failed to commit location: {str(e.orig)}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error during location creation: {str(e)}")

    async def add_locations_bulk(self, bulk_boundary: List[ServiceProviderLocationBoundary], db: AsyncSession) -> List[ServiceProviderLocationEntity]:
        location_entities = [
            ServiceProviderLocationEntity(
                provider_id=location.provider_id,
                full_address=location.location.full_address,
                geo_location=location.location.geo_location  # Storing as PostGIS point
            ) for location in bulk_boundary
        ]
        try:
            saved_locations = await self.repository.add_locations_bulk(location_entities, db)
            await db.commit()

            # Convert geo_points to Location objects before returning
            for loc in saved_locations:
                loc.geo_location = await self._convert_geo_point(loc.geo_location)
            return saved_locations
        except IntegrityError as e:
            await db.rollback()
            raise ValidationError(f"Failed to commit locations in bulk: {str(e.orig)}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error during bulk location creation: {str(e)}")

    async def remove_location(self, location_id: uuid.UUID, db: AsyncSession) -> None:
        try:
            await self.repository.remove_location(location_id, db)
            await db.commit()
        except ValueError as e:
            await db.rollback()
            raise ValidationError(f"Location removal failed: {str(e)}")
        except IntegrityError as e:
            await db.rollback()
            raise ValidationError(f"Failed to remove location: {str(e)}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error during location removal: {str(e)}")

    async def get_locations_by_provider_id(self, provider_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ServiceProviderLocationEntity]:
        try:
            locations = await self.repository.get_locations_by_provider_id(provider_id, db, skip, limit)

            # Convert geo_points to Location objects before returning
            for loc in locations:
                loc.geo_location =await self._convert_geo_point(loc.geo_location)
            return locations
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error fetching locations by provider: {str(e)}")

    async def get_all_locations(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ServiceProviderLocationEntity]:
        try:
            locations = await self.repository.get_all_locations(db, skip, limit)

            # Convert geo_points to Location objects before returning
            for loc in locations:
                loc.geo_location =await self._convert_geo_point(loc.geo_location)
            return locations
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error fetching all locations: {str(e)}")

    def _convert_geo_point(self, geo_point: WKBElement) -> Location:
        """Converts the PostGIS point (WKBElement) to the Location object."""
        point = wkb.loads(bytes(geo_point.data))
        return Location(latitude=point.y, longitude=point.x)
