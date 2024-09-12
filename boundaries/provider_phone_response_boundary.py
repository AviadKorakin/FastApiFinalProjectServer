from uuid import UUID

from pydantic import BaseModel

class ProviderPhoneResponseBoundary(BaseModel):
    phone_id: UUID
    provider_id: UUID
    phone_number: str
    class Config:
        from_attributes = True