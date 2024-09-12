from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base
import uuid


class NotificationEntity(Base):
    __tablename__ = "notifications"

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    message = Column(String, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, nullable=False)

    # Relationships
    user = relationship("UserEntity", back_populates="notifications")

    def __init__(self, user_id: uuid.UUID, message: str, status: str):
        self.user_id = user_id
        self.message = message
        self.status = status
        self.date = datetime.utcnow()

    def __eq__(self, other):
        return isinstance(other, NotificationEntity) and self.notification_id == other.notification_id

    def __str__(self):
        return f"NotificationEntity(notification_id='{self.notification_id}', user_id='{self.user_id}', message='{self.message}', status='{self.status}')"
