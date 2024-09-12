from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from entities.user_entity import UserEntity
from typing import List, Optional
import uuid

class UserRepository(ABC):

    @abstractmethod
    async def create(self, user: UserEntity, db: AsyncSession) -> UserEntity:
        pass

    @abstractmethod
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[UserEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, db: AsyncSession, user_id: uuid.UUID) -> Optional[UserEntity]:
        pass

    @abstractmethod
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    async def update(self, db: AsyncSession, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    async def update_user_details(self, user: UserEntity, db: AsyncSession) -> UserEntity:
        pass
