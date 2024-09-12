from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import time
import uuid

from boundaries.service_provider_create_boundary import ServiceProviderCreateBoundary
from dto.service_provider_dto import ServiceProviderDTO
from dto.open_service_provider_dto import OpenServiceProviderDTO
from entities.service_provider_entity import ServiceProviderEntity


class ServiceProviderService(ABC):

    @abstractmethod
    async def create_service_provider(self, boundary: ServiceProviderCreateBoundary, db: AsyncSession) -> ServiceProviderEntity:
        pass

    @abstractmethod
    async def update_service_provider(self, provider_id: uuid.UUID, name: Optional[str], service_type: Optional[str], email: Optional[str], db: AsyncSession) -> ServiceProviderEntity:
        pass

    @abstractmethod
    async def get_service_providers(
        self,
        provider_id: Optional[uuid.UUID],
        user_id: Optional[uuid.UUID],
        service_type: Optional[str],
        name: Optional[str],
        phone_number: Optional[str],
        day_of_week: Optional[str],
        desired_time: Optional[time],
        membership: Optional[str],
        longitude: Optional[float],
        latitude: Optional[float],
        radius_km: Optional[float],
        page: int,
        size: int,
        db: AsyncSession
    ) -> List[ServiceProviderDTO]:
        pass

    @abstractmethod
    async def get_open_service_providers(self, day_of_week: str, desired_time: time, page: int, size: int, db: AsyncSession) -> List[OpenServiceProviderDTO]:
        pass
