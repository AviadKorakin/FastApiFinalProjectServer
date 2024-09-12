from sqlalchemy import Column, String, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from entities.base import Base
from enums.membership_enum import MembershipEnum
import uuid


class ServiceProviderEntity(Base):
    __tablename__ = "service_providers"

    provider_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    email = Column(String, nullable=True)
    membership = Column(SQLAEnum(MembershipEnum), nullable=False)

    # Relationships
    users = relationship("UserProviderAssociationEntity", back_populates="provider", cascade="all, delete-orphan")
    service_requests = relationship("ServiceRequestEntity", back_populates="provider")
    phones = relationship("ProviderPhoneEntity", back_populates="provider", cascade="all, delete-orphan")
    working_hours = relationship("WorkingHoursEntity", back_populates="provider", cascade="all, delete-orphan")
    locations = relationship("ServiceProviderLocationEntity", back_populates="provider", cascade="all, delete-orphan")
    images = relationship("ServiceProviderImageEntity", back_populates="provider", cascade="all, delete-orphan")

    def __eq__(self, other):
        return isinstance(other, ServiceProviderEntity) and self.provider_id == other.provider_id

    def __str__(self):
        return f"ServiceProviderEntity(provider_id='{self.provider_id}', name='{self.name}', service_type='{self.service_type}')"
