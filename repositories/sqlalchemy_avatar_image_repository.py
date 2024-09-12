from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, select
from entities.avatar_image_entity import AvatarImageEntity
from repositories.avatar_image_repository import AvatarImageRepository
from typing import List
import uuid


class SQLAlchemyAvatarImageRepository(AvatarImageRepository):

    async def create(self, avatar_image: AvatarImageEntity, db: AsyncSession) -> AvatarImageEntity:
        db.add(avatar_image)
        await db.flush()  # Flush changes, but commit is handled in the service
        await db.refresh(avatar_image)
        return avatar_image

    async def get_all_by_user_id(self, user_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[AvatarImageEntity]:
        result = await db.execute(
            select(AvatarImageEntity).where(AvatarImageEntity.user_id == user_id).order_by(asc(AvatarImageEntity.folder_file_path))
            .offset(skip).limit(limit)
        )
        return result.scalars().all()
