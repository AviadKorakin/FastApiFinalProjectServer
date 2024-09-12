from uuid import UUID

from pydantic import BaseModel, FieldValidationInfo, field_validator
from datetime import time
from fastapi import HTTPException

from enums.day_of_week_enum import DayOfWeekEnum


class WorkingHoursUpdateBoundary(BaseModel):
    working_hours_id: UUID
    day_of_week: DayOfWeekEnum
    start_time: time = time(9, 0)  # Default value set to 09:00 AM
    end_time: time = time(17, 0)   # Default value set to 05:00 PM

    @field_validator('start_time', 'end_time', mode='before')
    def ensure_hours_minutes_format(cls, value: str, info: FieldValidationInfo) -> time:
        # Parse string input to time if it's not already a time object
        if isinstance(value, str):
            try:
                parsed_time = time.fromisoformat(value)  # Converts 'HH:MM' or 'HH:MM:SS' string to a time object
            except ValueError:
                raise HTTPException(status_code=400, detail='Invalid time format. Expected HH:MM.')
        else:
            parsed_time = value

        # Ensure the time has no seconds or microseconds
        if parsed_time.second != 0 or parsed_time.microsecond != 0:
            raise HTTPException(status_code=400, detail='Time must be in HH:MM format without seconds or microseconds.')

        return parsed_time

    class Config:
        from_attributes = True
