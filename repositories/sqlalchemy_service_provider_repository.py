from datetime import time

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, and_
from entities.service_provider_entity import ServiceProviderEntity
from entities.service_provider_location_entity import ServiceProviderLocationEntity
from entities.working_hours_entity import WorkingHoursEntity
from entities.provider_phone_entity import ProviderPhoneEntity
from entities.user_provider_association_entity import UserProviderAssociationEntity
from enums.day_of_week_enum import DayOfWeekEnum
from dto.service_provider_dto import ServiceProviderDTO
from dto.open_service_provider_dto import OpenServiceProviderDTO
from typing import Optional, List

from enums.membership_enum import MembershipEnum
from repositories.service_provider_repository import ServiceProviderRepository
from utils.location import Location
from geoalchemy2.elements import WKBElement
from shapely import wkb
from sqlalchemy.orm import selectinload
import uuid


class SQLAlchemyServiceProviderRepository(ServiceProviderRepository):
    async def save_service_provider(self, service_provider: ServiceProviderEntity, db: AsyncSession) -> ServiceProviderEntity:
        db.add(service_provider)
        await db.flush()
        await db.refresh(service_provider)
        return service_provider

    async def add_users(self, users: List[UserProviderAssociationEntity], db: AsyncSession) -> None:
        db.add_all(users)
        await db.flush()

    async def add_phones(self, phones: List[ProviderPhoneEntity], db: AsyncSession) -> None:
        db.add_all(phones)
        await db.flush()

    async def add_working_hours(self, working_hours: List[WorkingHoursEntity], db: AsyncSession) -> None:
        db.add_all(working_hours)
        await db.flush()

    async def add_locations(self, locations: List[ServiceProviderLocationEntity], db: AsyncSession) -> None:
        db.add_all(locations)
        await db.flush()

    async def update_service_provider(self, provider: ServiceProviderEntity, db: AsyncSession) -> ServiceProviderEntity:
        await db.flush()
        await db.refresh(provider)
        return provider

    async def get_by_id(self, provider_id: uuid.UUID, db: AsyncSession) -> Optional[ServiceProviderEntity]:
        result = await db.execute(
            select(ServiceProviderEntity)
            .filter_by(provider_id=provider_id))
        return result.scalars().first()

    async def get_service_providers(
            self, provider_id: Optional[uuid.UUID], user_id: Optional[uuid.UUID], service_type: Optional[str],
            name: Optional[str], phone_number: Optional[str], day_of_week: Optional[DayOfWeekEnum],
            desired_time: Optional[time], membership: Optional[str], longitude: Optional[float],
            latitude: Optional[float], radius_km: Optional[float], page: int, size: int, db: AsyncSession
    ) -> List[ServiceProviderDTO]:

        # Build the query with filters
        query = select(ServiceProviderEntity).options(
            selectinload(ServiceProviderEntity.users),
            selectinload(ServiceProviderEntity.phones),
            selectinload(ServiceProviderEntity.working_hours),
            selectinload(ServiceProviderEntity.locations)
        )

        # Filters
        if provider_id:
            query = query.where(ServiceProviderEntity.provider_id == provider_id)
        if user_id:
            query = query.join(ServiceProviderEntity.users).where(ServiceProviderEntity.users.any(user_id=user_id))
        if service_type:
            query = query.where(ServiceProviderEntity.service_type == service_type)
        if name:
            query = query.where(func.lower(ServiceProviderEntity.name).contains(name.lower()))
        if phone_number:
            query = query.join(ServiceProviderEntity.phones).where(ProviderPhoneEntity.phone_number == phone_number)
        if membership:
            query = query.where(ServiceProviderEntity.membership == membership)

        # Working hours filter
        if day_of_week and desired_time:
            query = query.join(ServiceProviderEntity.working_hours).where(
                and_(
                    WorkingHoursEntity.day_of_week == day_of_week,
                    WorkingHoursEntity.start_time <= desired_time,
                    WorkingHoursEntity.end_time >= desired_time
                )
            )

        # Geo-location filter and ordering by distance
        if longitude is not None and latitude is not None:
            point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
            if radius_km is not None:
                query = query.join(ServiceProviderEntity.locations).where(
                    func.ST_DWithin(ServiceProviderLocationEntity.geo_location, point, radius_km * 1000)
                )
            query = query.order_by(func.ST_Distance(ServiceProviderLocationEntity.geo_location, point))

        # Additional ordering: name, service type, membership
        query = query.order_by(
            func.lower(ServiceProviderEntity.name).asc(),
            ServiceProviderEntity.service_type.asc(),
        )

        # Apply pagination
        query = query.offset((page - 1) * size).limit(size)

        # Execute query
        result = await db.execute(query)
        providers = result.scalars().all()

        # Sort working hours for each provider by the rank of the day of the week
        for provider in providers:
            provider.working_hours.sort(key=lambda wh: wh.day_of_week.rank)

        # In-memory sorting of providers using MembershipEnum and DayOfWeekEnum
        providers.sort(key=lambda provider: (
            MembershipEnum(provider.membership),
        ))

        if providers:
            await self._convert_geo_locations_for_providers(providers)

        return [ServiceProviderDTO(**provider.__dict__) for provider in providers]

    async def get_open_service_providers(
            self, day_of_week: DayOfWeekEnum, desired_time: time, page: int, size: int, db: AsyncSession
    ) -> List[OpenServiceProviderDTO]:

        query = select(ServiceProviderEntity).join(ServiceProviderEntity.working_hours).where(
            and_(
                WorkingHoursEntity.day_of_week == day_of_week,
                WorkingHoursEntity.start_time <= desired_time,
                WorkingHoursEntity.end_time >= desired_time
            )
        ).options(
            selectinload(ServiceProviderEntity.users),
            selectinload(ServiceProviderEntity.phones),
            selectinload(ServiceProviderEntity.working_hours),
            selectinload(ServiceProviderEntity.locations)
        )

        # Additional ordering: name, service type, membership
        query = query.order_by(
            func.lower(ServiceProviderEntity.name).asc(),
            ServiceProviderEntity.service_type.asc(),
            ServiceProviderEntity.membership.asc(),
            WorkingHoursEntity.day_of_week
        )

        # Apply pagination
        query = query.offset((page - 1) * size).limit(size)

        # Execute query
        result = await db.execute(query)
        open_providers = result.scalars().all()

        # In-memory sorting of providers using MembershipEnum
        open_providers.sort(key=lambda provider: MembershipEnum(provider.membership))

        if open_providers:
            await self._convert_geo_locations_for_providers(open_providers)

        return [OpenServiceProviderDTO(**provider.__dict__)  for provider in open_providers]

    async def _convert_geo_locations_for_providers(self, providers: List[ServiceProviderEntity]) -> None:
        for provider in providers:
            if provider.locations:
                for loc in provider.locations:
                    await self._convert_geo_point(loc)

    async def _convert_geo_point(self, loc) -> None:
        if isinstance(loc.geo_location, WKBElement):
            point = wkb.loads(bytes(loc.geo_location.data))
            loc.geo_location = Location(latitude=point.y, longitude=point.x)
