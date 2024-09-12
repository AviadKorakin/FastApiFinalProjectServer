import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base

class PetImageEntity(Base):
    __tablename__ = "pet_images"

    # UUID primary key for the image
    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.pet_id"), nullable=False)
    file_path = Column(String, nullable=False)  # Not primary key anymore
    url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to Pet
    pet = relationship("PetEntity", back_populates="pet_images")

    def __init__(self, pet_id: uuid.UUID, url: str, file_path: str, created_at: datetime = None):
        self.pet_id = pet_id
        self.url = url
        self.file_path = file_path
        self.created_at = created_at or datetime.utcnow()

    def __eq__(self, other):
        if isinstance(other, PetImageEntity):
            return self.image_id == other.image_id
        return False

    def __str__(self):
        return f"PetImageEntity(image_id='{self.image_id}', pet_id='{self.pet_id}', url='{self.url}', file_path='{self.file_path}', created_at='{self.created_at}')"
