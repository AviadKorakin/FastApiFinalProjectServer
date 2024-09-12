
from pydantic import BaseModel, Field, UUID4
from typing import Optional
from boundaries.lost_pet_report_boundary import Location


class UpdateLostPetReportBoundary(BaseModel):
    geo_location: Optional[Location] = Field(None, description="Updated location of the lost pet")
    description: Optional[str] = Field(None, description="Updated description of the lost pet report")
    status: Optional[str] = Field(None, description="Updated status of the report (e.g., 'lost', 'found')")

    class Config:
        from_attributes = True