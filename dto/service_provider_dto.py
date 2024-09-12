from uuid import UUID

from pydantic import BaseModel
from typing import List
from boundaries.user_provider_boundary import UserProviderBoundary
from boundaries.provider_phone_boundary import ProviderPhoneBoundary
from boundaries.working_hours_boundary import WorkingHoursBoundary
from boundaries.service_provider_location_boundary import ServiceProviderLocationBoundary

class ServiceProviderDTO(BaseModel):
    provider_id: UUID
    name: str
    service_type: str
    email: str
    phones: List[ProviderPhoneBoundary]
    working_hours: List[WorkingHoursBoundary]
    locations: List[ServiceProviderLocationBoundary]  # Added locations field

    class Config:
        from_attributes = True
