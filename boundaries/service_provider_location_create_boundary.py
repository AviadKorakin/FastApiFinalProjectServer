from uuid import UUID

from pydantic import BaseModel
from boundaries.service_provider_location_boundary import ServiceProviderLocationBoundary

class ServiceProviderLocationCreateBoundary(BaseModel):
    provider_id: UUID  # Provider ID
    location: ServiceProviderLocationBoundary  # Wrapping the existing boundary

    class Config:
        from_attributes = True
