from abc import ABC, abstractmethod
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from entities.user_entity import UserEntity
from typing import List, Optional
import uuid

class UserService(ABC):

    @abstractmethod
    async def create_user(self, email: str, password: str, first_name: str, last_name: str, role: str,
                          phone_number: str, db: AsyncSession = None) -> tuple[UserEntity, str]:
        pass
    @abstractmethod
    async def send_verification_email(self, email: str, verification_url: str):
        pass

    @abstractmethod
    async def login_user(self, email: str, password: str, db: AsyncSession) -> Optional[UserEntity]:
        pass

    @abstractmethod
    async def verify_email(self, user_id: uuid.UUID, token: str, db: AsyncSession) -> bool:
        pass

    @abstractmethod
    async def reset_token(self, email: str, db: AsyncSession) -> tuple[uuid.UUID, str]:
        pass

    @abstractmethod
    async def update_user_details(self, user_id: uuid.UUID, old_password: str, new_password: Optional[str],
                                  first_name: Optional[str], last_name: Optional[str],
                                  phone_number: Optional[str], db: AsyncSession) -> UserEntity:
        pass

    @abstractmethod
    async def get_users(self, db: AsyncSession, page: int = 1, size: int = 10) -> List[UserEntity]:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: uuid.UUID, db: AsyncSession) -> Optional[UserEntity]:
        pass
