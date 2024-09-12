# Location class for geo-location fields
from pydantic import BaseModel, field_validator


class Location(BaseModel):
    latitude: float
    longitude: float

    @field_validator('latitude')
    def validate_latitude(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Latitude must be between -90 and 90.')
        return v

    @field_validator('longitude')
    def validate_longitude(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError('Longitude must be between -180 and 180.')
        return v