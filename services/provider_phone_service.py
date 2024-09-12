from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid
from entities.provider_phone_entity import ProviderPhoneEntity
from boundaries.provider_phone_boundary import ProviderPhoneBoundary

class ProviderPhoneService(ABC):

    @abstractmethod
    async def add_phone(self, provider_id: uuid.UUID, phone_boundary: ProviderPhoneBoundary, db: AsyncSession) -> ProviderPhoneEntity:
        pass

    @abstractmethod
    async def add_phones_bulk(self, provider_id: uuid.UUID, phones: List[ProviderPhoneBoundary], db: AsyncSession) -> List[ProviderPhoneEntity]:
        pass

    @abstractmethod
    async def remove_phone(self, phone_id: uuid.UUID, db: AsyncSession) -> None:
        pass

    @abstractmethod
    async def get_phones_by_provider_id(self, provider_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ProviderPhoneEntity]:
        pass

    @abstractmethod
    async def get_all_phones(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[ProviderPhoneEntity]:
        pass
