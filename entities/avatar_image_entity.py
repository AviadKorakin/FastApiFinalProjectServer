from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base
import uuid

class AvatarImageEntity(Base):
    __tablename__ = "avatar_images"

    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    s3_file_path = Column(String, nullable=False)  # Full S3 path
    folder_file_path = Column(String, nullable=False, unique=True)  # File path inside the folder (unique)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to UserEntity
    user = relationship("UserEntity", back_populates="avatar_images")

    def __init__(self, s3_file_path: str, folder_file_path: str, user_id: uuid.UUID, url: str, created_at: datetime = None):
        self.s3_file_path = s3_file_path
        self.folder_file_path = folder_file_path
        self.user_id = user_id
        self.url = url
        self.created_at = created_at or datetime.utcnow()

    def __eq__(self, other):
        if isinstance(other, AvatarImageEntity):
            return self.image_id == other.image_id
        return False

    def __str__(self):
        return f"AvatarImageEntity(image_id='{self.image_id}', s3_file_path='{self.s3_file_path}', folder_file_path='{self.folder_file_path}', user_id='{self.user_id}', url='{self.url}', created_at='{self.created_at}')"
