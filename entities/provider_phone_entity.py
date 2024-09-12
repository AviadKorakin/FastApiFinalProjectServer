from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from entities.base import Base
import uuid


class ProviderPhoneEntity(Base):
    __tablename__ = "provider_phones"

    phone_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("service_providers.provider_id"), nullable=False)
    phone_number = Column(String, nullable=False)

    # Relationship to ServiceProviderEntity
    provider = relationship("ServiceProviderEntity", back_populates="phones")

    # Unique constraint to prevent duplicate phone numbers for the same provider
    __table_args__ = (UniqueConstraint('provider_id', 'phone_number', name='uq_provider_phone_number'),)

    def __eq__(self, other):
        return isinstance(other, ProviderPhoneEntity) and self.phone_id == other.phone_id

    def __str__(self):
        return f"ProviderPhoneEntity(phone_id='{self.phone_id}', provider_id='{self.provider_id}', phone_number='{self.phone_number}')"
