from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from entities.user_provider_association_entity import UserProviderAssociationEntity

class UserProviderRepository(ABC):

    @abstractmethod
    async def add_user_provider(self, association: UserProviderAssociationEntity, db: AsyncSession) -> UserProviderAssociationEntity:
        """Add a single user-provider association."""
        pass

    @abstractmethod
    async def add_user_providers_bulk(self, associations: List[UserProviderAssociationEntity], db: AsyncSession) -> List[UserProviderAssociationEntity]:
        """Add multiple user-provider associations in bulk."""
        pass

    @abstractmethod
    async def remove_user_provider(self, user_id: UUID, provider_id: UUID, db: AsyncSession) -> None:
        """Remove a user-provider association by user_email and provider_id."""
        pass

    @abstractmethod
    async def get_by_filters(self, user_id: Optional[UUID], provider_id: Optional[UUID], role: Optional[str], db: AsyncSession, skip: int = 0, limit: int = 10) -> List[UserProviderAssociationEntity]:
        """Get user-provider associations by filters such as user_email, provider_id, and role."""
        pass
