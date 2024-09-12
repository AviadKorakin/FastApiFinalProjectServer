from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from entities.service_provider_location_entity import ServiceProviderLocationEntity
from typing import List
import uuid


class ServiceProviderLocationRepository(ABC):

    @abstractmethod
    async def add_location(self, location: ServiceProviderLocationEntity, db: AsyncSession) -> ServiceProviderLocationEntity:
        pass

    @abstractmethod
    async def add_locations_bulk(self, locations: List[ServiceProviderLocationEntity], db: AsyncSession) -> List[ServiceProviderLocationEntity]:
        pass

    @abstractmethod
    async def remove_location(self, location_id: uuid.UUID, db: AsyncSession) -> None:
        pass

    @abstractmethod
    async def get_locations_by_provider_id(self, provider_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ServiceProviderLocationEntity]:
        pass

    @abstractmethod
    async def get_all_locations(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ServiceProviderLocationEntity]:
        pass
