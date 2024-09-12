from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from entities.user_provider_association_entity import UserProviderAssociationEntity
from boundaries.user_provider_boundary import UserProviderBoundary

class UserProviderService(ABC):
    @abstractmethod
    async def add_user_provider(self, boundary: UserProviderBoundary, provider_id: str, db: AsyncSession) -> UserProviderAssociationEntity:
        pass

    @abstractmethod
    async def add_user_providers_bulk(self, users: List[UserProviderBoundary], provider_id: str, db: AsyncSession) -> List[UserProviderAssociationEntity]:
        pass

    @abstractmethod
    async def remove_user_provider(self, user_email: str, provider_id: str, db: AsyncSession) -> None:
        pass

    @abstractmethod
    async def get_user_providers(self, user_email: Optional[str], provider_id: Optional[str], role: Optional[str], db: AsyncSession, skip: int = 0, limit: int = 10) -> List[UserProviderAssociationEntity]:
        pass
