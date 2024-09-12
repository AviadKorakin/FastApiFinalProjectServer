
from typing import Optional
from pydantic import Field, BaseModel
from utils.location import Location  # Location will have latitude, longitude fields

class UpdateFoundPetReportBoundary(BaseModel):
    geo_location: Optional[Location] = Field(None, description="Updated location of the lost pet")
    description: Optional[str] = Field(None, description="Updated description of the lost pet report")

    class Config:
        from_attributes = True