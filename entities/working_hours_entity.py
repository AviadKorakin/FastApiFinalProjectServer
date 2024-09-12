from datetime import time

from sqlalchemy import Column,Time, ForeignKey, UniqueConstraint, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from entities.base import Base
from enums.day_of_week_enum import DayOfWeekEnum
import uuid


class WorkingHoursEntity(Base):
    __tablename__ = "working_hours"

    working_hours_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("service_providers.provider_id"), nullable=False)
    day_of_week = Column(SQLAEnum(DayOfWeekEnum), nullable=False)  # Enum for day of the week
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    # Relationship to ServiceProviderEntity
    provider = relationship("ServiceProviderEntity", back_populates="working_hours")

    # Unique constraint to ensure no duplicate working hours for the same provider and day
    __table_args__ = (UniqueConstraint('provider_id', 'day_of_week', name='uq_provider_day'),)

    def __init__(self, provider_id: uuid.UUID, day_of_week: DayOfWeekEnum, start_time: time, end_time: time):
        self.provider_id = provider_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other):
        return isinstance(other, WorkingHoursEntity) and self.working_hours_id == other.working_hours_id

    def __str__(self):
        return f"WorkingHoursEntity(working_hours_id='{self.working_hours_id}', provider_id='{self.provider_id}', day_of_week='{self.day_of_week}')"
