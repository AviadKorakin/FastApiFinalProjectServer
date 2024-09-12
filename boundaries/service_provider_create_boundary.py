from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr
from boundaries.provider_phone_boundary import ProviderPhoneBoundary
from boundaries.user_provider_boundary import UserProviderBoundary
from boundaries.working_hours_boundary import WorkingHoursBoundary
from boundaries.service_provider_location_boundary import ServiceProviderLocationBoundary
from enums.membership_enum import MembershipEnum

class ServiceProviderCreateBoundary(BaseModel):
    name: str
    service_type: str
    email: Optional[EmailStr]  # Email is now optional
    membership: MembershipEnum = MembershipEnum.FREE  # Default to Free

    # Enforce at least 1 user, phone, and working hours entry
    users: List[UserProviderBoundary] = Field(..., min_items=1)
    phones: List[ProviderPhoneBoundary] = Field(..., min_items=1)
    working_hours: List[WorkingHoursBoundary] = Field(..., min_items=1)
    locations: List[ServiceProviderLocationBoundary] = Field(..., min_items=1)  # Added locations

    class Config:
        from_attributes = True
