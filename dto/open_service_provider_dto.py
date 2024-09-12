from uuid import UUID

from pydantic import BaseModel
from typing import List
from boundaries.working_hours_boundary import WorkingHoursBoundary
from boundaries.service_provider_location_boundary import ServiceProviderLocationBoundary

class OpenServiceProviderDTO(BaseModel):
    provider_id: UUID
    name: str
    service_type: str
    working_hours: List[WorkingHoursBoundary]
    locations: List[ServiceProviderLocationBoundary]  # Added locations field

    class Config:
        from_attributes = True
