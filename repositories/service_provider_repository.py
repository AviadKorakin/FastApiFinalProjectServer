import uuid
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from entities.service_provider_entity import ServiceProviderEntity
from entities.user_provider_association_entity import UserProviderAssociationEntity
from entities.provider_phone_entity import ProviderPhoneEntity
from entities.working_hours_entity import WorkingHoursEntity
from entities.service_provider_location_entity import ServiceProviderLocationEntity
from dto.service_provider_dto import ServiceProviderDTO
from dto.open_service_provider_dto import OpenServiceProviderDTO
from datetime import time
from enums.day_of_week_enum import DayOfWeekEnum


class ServiceProviderRepository(ABC):

    @abstractmethod
    async def save_service_provider(self, service_provider: ServiceProviderEntity, db: AsyncSession) -> ServiceProviderEntity:
        pass

    @abstractmethod
    async def add_users(self, users: List[UserProviderAssociationEntity], db: AsyncSession) -> None:
        pass

    @abstractmethod
    async def add_phones(self, phones: List[ProviderPhoneEntity], db: AsyncSession) -> None:
        pass

    @abstractmethod
    async def add_working_hours(self, working_hours: List[WorkingHoursEntity], db: AsyncSession) -> None:
        pass

    @abstractmethod
    async def add_locations(self, locations: List[ServiceProviderLocationEntity], db: AsyncSession) -> None:
        pass

    @abstractmethod
    async def update_service_provider(self, provider: ServiceProviderEntity, db: AsyncSession) -> ServiceProviderEntity:
        pass

    @abstractmethod
    async def get_by_id(self, provider_id: uuid.UUID, db: AsyncSession) -> Optional[ServiceProviderEntity]:
        pass

    @abstractmethod
    async def get_service_providers(
        self,
        provider_id: Optional[str],
        user_id: Optional[str],
        service_type: Optional[str],
        name: Optional[str],
        phone_number: Optional[str],
        day_of_week: Optional[DayOfWeekEnum],
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
    async def get_open_service_providers(self, day_of_week: DayOfWeekEnum, desired_time: time, page: int, size: int, db: AsyncSession) -> List[OpenServiceProviderDTO]:
        pass
