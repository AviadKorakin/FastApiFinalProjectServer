from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from entities.service_provider_location_entity import ServiceProviderLocationEntity
from boundaries.service_provider_location_create_boundary import ServiceProviderLocationCreateBoundary
from boundaries.service_provider_location_boundary import ServiceProviderLocationBoundary
from typing import List
import uuid


class ServiceProviderLocationService(ABC):

    @abstractmethod
    async def add_location(self, location_boundary: ServiceProviderLocationCreateBoundary, db: AsyncSession) -> ServiceProviderLocationEntity:
        pass

    @abstractmethod
    async def add_locations_bulk(self, bulk_boundary: List[ServiceProviderLocationBoundary], db: AsyncSession) -> List[ServiceProviderLocationEntity]:
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
