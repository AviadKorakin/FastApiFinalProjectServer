import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from entities.service_provider_location_entity import ServiceProviderLocationEntity
from repositories.service_provider_location_repository import ServiceProviderLocationRepository


class SQLAlchemyServiceProviderLocationRepository(ServiceProviderLocationRepository):

    async def add_location(self, location: ServiceProviderLocationEntity, db: AsyncSession) -> ServiceProviderLocationEntity:
        db.add(location)
        await db.flush()  # Save the location to the database
        await db.refresh(location)  # Refresh to get the latest data from the database
        return location

    async def add_locations_bulk(self, locations: List[ServiceProviderLocationEntity], db: AsyncSession) -> List[ServiceProviderLocationEntity]:
        db.add_all(locations)
        await db.flush()  # Save the bulk locations to the database
        return locations

    async def remove_location(self, location_id: uuid.UUID, db: AsyncSession) -> None:
        location = await db.get(ServiceProviderLocationEntity, location_id)
        if location:
            await db.delete(location)
            await db.flush()  # Execute deletion
        else:
            raise ValueError(f"Location with ID {location_id} not found.")

    async def get_locations_by_provider_id(self, provider_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ServiceProviderLocationEntity]:
        stmt = select(ServiceProviderLocationEntity).filter_by(provider_id=provider_id)\
                                                    .order_by(ServiceProviderLocationEntity.full_address)\
                                                    .offset(skip)\
                                                    .limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_all_locations(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ServiceProviderLocationEntity]:
        stmt = select(ServiceProviderLocationEntity).order_by(ServiceProviderLocationEntity.provider_id, ServiceProviderLocationEntity.full_address)\
                                                    .offset(skip)\
                                                    .limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
