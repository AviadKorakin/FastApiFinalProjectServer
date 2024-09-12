from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field, BaseModel

from utils.location import Location


class LostPetReportBoundary(BaseModel):
    report_id: UUID
    pet_id: UUID
    user_id: UUID
    report_date: datetime = Field(default_factory=datetime.utcnow)
    geo_location: Optional[Location] = Field(
        None,
        example={"latitude": 40.73061, "longitude": -73.935242},
        description="Geo-location in the format {latitude: float, longitude: float}"
    )
    description: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True