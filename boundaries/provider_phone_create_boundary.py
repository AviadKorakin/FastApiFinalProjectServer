from uuid import UUID

from pydantic import BaseModel
from boundaries.provider_phone_boundary import ProviderPhoneBoundary


class ProviderPhoneCreateBoundary(BaseModel):
    provider_id: UUID
    phone:ProviderPhoneBoundary
    class Config:
        from_attributes = True
