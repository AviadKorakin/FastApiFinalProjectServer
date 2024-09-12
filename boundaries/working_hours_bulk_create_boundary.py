from typing import List
from uuid import UUID

from pydantic import BaseModel
from boundaries.working_hours_boundary import WorkingHoursBoundary

class WorkingHoursBulkCreateBoundary(BaseModel):
    provider_id: UUID
    working_hours_list: List[WorkingHoursBoundary]
    class Config:
        from_attributes = True