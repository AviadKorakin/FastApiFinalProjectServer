from uuid import UUID

from pydantic import BaseModel
from utils.location import Location

class ServiceProviderLocationResponseBoundary(BaseModel):
    location_id: UUID
    provider_id: UUID
    full_address: str
    geo_location: Location  # Using the Location class for geo-location

    class Config:
        from_attributes = True
