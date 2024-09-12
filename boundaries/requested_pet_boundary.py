from uuid import UUID

from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import date

class RequestedPetBoundary(BaseModel):
    user_id: Optional[UUID] = None
    name: str  # Add name as required
    species: str
    breed: Optional[str] = None
    date_of_birth: Optional[date] = None
    main_color: Optional[str] = None
    pet_details: Optional[Dict[str, str]] = Field(default_factory=dict)

    class Config:
        from_attributes = True
