from typing import List
from uuid import UUID

from pydantic import BaseModel

from boundaries.service_provider_location_boundary import ServiceProviderLocationBoundary

class ServiceProviderLocationBulkCreateBoundary(BaseModel):
    provider_id:UUID
    locations: List[ServiceProviderLocationBoundary]  # List of locations with provider_id and boundary

    class Config:
        from_attributes = True
