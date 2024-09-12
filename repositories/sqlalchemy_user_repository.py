import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from entities.user_entity import UserEntity
from repositories.user_repository import UserRepository


class SQLAlchemyUserRepository(UserRepository):

    async def create(self, user: UserEntity, db: AsyncSession) -> UserEntity:
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[UserEntity]:
        result = await db.execute(
            select(UserEntity)
            .order_by(UserEntity.email)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, user_id: uuid.UUID) -> Optional[UserEntity]:
        result = await db.execute(select(UserEntity).filter_by(user_id=user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[UserEntity]:
        result = await db.execute(select(UserEntity).filter_by(email=email))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, user: UserEntity) -> UserEntity:
        await db.merge(user)
        await db.flush()
        await db.refresh(user)
        return user

    async def update_user_details(self, user: UserEntity, db: AsyncSession) -> UserEntity:
        await db.flush()
        await db.refresh(user)
        return user
