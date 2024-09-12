from abc import ABC, abstractmethod
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from entities.avatar_image_entity import AvatarImageEntity

class AvatarImageService(ABC):

    @abstractmethod
    def generate_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        """Generate a presigned URL for image upload, enforcing JPEG content type."""
        pass

    @abstractmethod
    async def upload_image(self, file_path: str, s3_path: str, user_id: uuid.UUID,
                           db: AsyncSession) -> AvatarImageEntity:
        """Confirm avatar image upload by storing metadata in the database."""
        pass

    @abstractmethod
    async def get_images_by_user(self, user_id: uuid.UUID, page: int, size: int, db: AsyncSession) -> List[
        AvatarImageEntity]:
        """Retrieve all avatar images for a user, with pagination."""
        pass
