from uuid import UUID

from pydantic import BaseModel
from boundaries.working_hours_boundary import WorkingHoursBoundary

class WorkingHoursCreateBoundary(BaseModel):
    provider_id: UUID
    working_hours: WorkingHoursBoundary
    class Config:
        from_attributes = True

