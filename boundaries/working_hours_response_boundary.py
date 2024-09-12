# boundaries/working_hours_response_boundary.py
from uuid import UUID

from pydantic import BaseModel
from datetime import time
from enums.day_of_week_enum import DayOfWeekEnum

class WorkingHoursResponseBoundary(BaseModel):
    working_hours_id: UUID
    day_of_week: DayOfWeekEnum
    start_time: time
    end_time: time
    provider_id: UUID

    class Config:
        from_attributes = True
