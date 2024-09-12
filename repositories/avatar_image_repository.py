from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid
from entities.avatar_image_entity import AvatarImageEntity


class AvatarImageRepository(ABC):

    @abstractmethod
    async def create(self, avatar_image: AvatarImageEntity, db: AsyncSession) -> AvatarImageEntity:
        """Create a new AvatarImageEntity in the database."""
        pass

    @abstractmethod
    async def get_all_by_user_id(self, user_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[
        AvatarImageEntity]:
        """Retrieve all avatar images for a user, with pagination."""
        pass
