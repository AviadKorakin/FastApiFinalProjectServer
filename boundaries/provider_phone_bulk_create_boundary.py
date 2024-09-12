from typing import List
from uuid import UUID

from pydantic import BaseModel
from boundaries.provider_phone_boundary import ProviderPhoneBoundary

class ProviderPhoneBulkCreateBoundary(BaseModel):
    provider_id: UUID
    phones: List[ProviderPhoneBoundary]

    class Config:
        from_attributes = True