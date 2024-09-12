from sqlalchemy import Column, String, Enum as SQLAEnum, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from entities.base import Base
from enums.role_enum import RoleEnum

class UserEntity(Base):
    __tablename__ = "users"

    # New UUID-based user ID
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    role = Column(SQLAEnum(RoleEnum), nullable=False)
    hashed_password = Column(String, nullable=False)
    email_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    token_expiration = Column(DateTime(timezone=True), nullable=True)

    # Relationships to other entities
    providers = relationship("UserProviderAssociationEntity", back_populates="user", cascade="all, delete-orphan")
    pets = relationship("PetEntity", back_populates="user")
    service_requests = relationship("ServiceRequestEntity", back_populates="user", cascade="all, delete-orphan")
    lost_pet_reports = relationship("LostPetReportEntity", back_populates="user")
    notifications = relationship("NotificationEntity", back_populates="user", cascade="all, delete-orphan")
    avatar_images = relationship("AvatarImageEntity", back_populates="user", cascade="all, delete-orphan")
    found_pet_reports = relationship("FoundPetReportEntity", back_populates="user")

    def __eq__(self, other):
        if isinstance(other, UserEntity):
            return self.email == other.email
        return False

    def __str__(self):
        return f"UserEntity(user_id='{self.user_id}', email='{self.email}', role='{self.role}', email_verified='{self.email_verified}')"
