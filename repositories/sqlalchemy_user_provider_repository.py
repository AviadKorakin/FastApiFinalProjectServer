from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from entities.user_provider_association_entity import UserProviderAssociationEntity
from repositories.user_provider_repository import UserProviderRepository
from errors.validation_error import ValidationError
from typing import List, Optional
import uuid

class SQLAlchemyUserProviderRepository(UserProviderRepository):

    async def add_user_provider(self, association: UserProviderAssociationEntity, db: AsyncSession) -> UserProviderAssociationEntity:
        db.add(association)
        await db.flush()
        await db.refresh(association)
        return association

    async def add_user_providers_bulk(self, associations: List[UserProviderAssociationEntity], db: AsyncSession) -> List[UserProviderAssociationEntity]:
        db.add_all(associations)
        await db.flush()
        return associations

    async def remove_user_provider(self, user_id: uuid.UUID, provider_id: uuid.UUID, db: AsyncSession) -> None:
        query = select(UserProviderAssociationEntity).filter(
            UserProviderAssociationEntity.user_id == user_id,
            UserProviderAssociationEntity.provider_id == provider_id
        )
        result = await db.execute(query)
        association = result.scalar_one_or_none()

        if not association:
            raise ValidationError(f"User-provider association with user_email '{user_id}' and provider_id '{provider_id}' not found.")

        await db.delete(association)
        await db.flush()

    async def get_by_filters(self, user_id: Optional[uuid.UUID], provider_id: Optional[uuid.UUID], role: Optional[str], db: AsyncSession, skip: int = 0, limit: int = 10) -> List[UserProviderAssociationEntity]:
        query = select(UserProviderAssociationEntity)

        if user_id:
            query = query.where(UserProviderAssociationEntity.user_id == user_id)
        if provider_id:
            query = query.where(UserProviderAssociationEntity.provider_id == provider_id)
        if role:
            query = query.where(UserProviderAssociationEntity.role == role)

        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
