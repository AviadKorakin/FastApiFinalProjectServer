from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base
import uuid


class ServiceProviderImageEntity(Base):
    __tablename__ = "service_provider_images"

    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("service_providers.provider_id"), nullable=False)
    s3_file_path = Column(String, nullable=False)  # Full S3 path
    url = Column(String, nullable=False)  # Public URL of the image
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to ServiceProviderEntity
    provider = relationship("ServiceProviderEntity", back_populates="images")

    def __init__(self, provider_id: uuid.UUID, s3_file_path: str, url: str):
        self.provider_id = provider_id
        self.s3_file_path = s3_file_path
        self.url = url
        self.created_at = datetime.utcnow()

    def __eq__(self, other):
        return isinstance(other, ServiceProviderImageEntity) and self.image_id == other.image_id

    def __str__(self):
        return f"ServiceProviderImageEntity(image_id='{self.image_id}', provider_id='{self.provider_id}', url='{self.url}', created_at='{self.created_at}')"
