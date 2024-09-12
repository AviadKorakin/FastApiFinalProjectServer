from typing import Optional
from uuid import UUID

from pydantic import BaseModel

class ServiceProviderBoundary(BaseModel):
    provider_id: UUID
    name: str
    service_type: str
    email: Optional[str]  # Email is now optional
    membership: str  # Include membership in the return

    class Config:
        from_attributes = True  # Enables ORM mode
