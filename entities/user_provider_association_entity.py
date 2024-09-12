from sqlalchemy import Column, ForeignKey, UniqueConstraint, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from entities.base import Base
from enums.user_provider_role_enum import UserProviderRoleEnum
import uuid


class UserProviderAssociationEntity(Base):
    __tablename__ = 'user_provider_association'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), primary_key=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey('service_providers.provider_id'), primary_key=True)
    role = Column(SQLAEnum(UserProviderRoleEnum), nullable=False)

    # Unique constraint to prevent duplicate associations
    __table_args__ = (UniqueConstraint('user_id', 'provider_id', name='uq_user_provider'),)

    # Relationships
    user = relationship("UserEntity", back_populates="providers")
    provider = relationship("ServiceProviderEntity", back_populates="users")

    def __eq__(self, other):
        return isinstance(other, UserProviderAssociationEntity) and self.user_id == other.user_id and self.provider_id == other.provider_id

    def __str__(self):
        return f"UserProviderAssociation(user_id='{self.user_id}', provider_id='{self.provider_id}', role='{self.role}')"
