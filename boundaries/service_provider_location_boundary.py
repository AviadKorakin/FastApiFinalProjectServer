from pydantic import BaseModel
from utils.location import Location

class ServiceProviderLocationBoundary(BaseModel):
    full_address: str
    geo_location: Location  # Using the Location class for geo-location

    class Config:
        from_attributes = True
