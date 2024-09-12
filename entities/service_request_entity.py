from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base
import uuid


class ServiceRequestEntity(Base):
    __tablename__ = "service_requests"

    request_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("service_providers.provider_id"), nullable=False)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.pet_id"), nullable=True)
    request_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False)

    # Relationships
    user = relationship("UserEntity", back_populates="service_requests")
    provider = relationship("ServiceProviderEntity", back_populates="service_requests")
    pet = relationship("PetEntity", back_populates="service_requests")

    def __eq__(self, other):
        return isinstance(other, ServiceRequestEntity) and self.request_id == other.request_id

    def __str__(self):
        return f"ServiceRequestEntity(request_id='{self.request_id}', user_id='{self.user_id}', provider_id='{self.provider_id}', pet_id='{self.pet_id}')"
