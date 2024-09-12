from uuid import UUID

from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import date

class PetBoundary(BaseModel):
    pet_id: UUID
    user_id: UUID
    name: str  # Add name to the response boundary
    species: str
    breed: Optional[str] = None
    date_of_birth: Optional[date] = None
    main_color: Optional[str] = None
    pet_details: Optional[Dict[str, str]] = Field(default_factory=dict)

    class Config:
        from_attributes = True
