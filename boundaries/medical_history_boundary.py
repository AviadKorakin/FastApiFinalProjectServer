from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

class MedicalHistoryBoundary(BaseModel):
    record_id: UUID
    pet_id: UUID
    visit_date: datetime = datetime.utcnow()
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    notes: Optional[str] = None
    veterinarian_name: Optional[str] = None

    class Config:
        from_attributes = True
