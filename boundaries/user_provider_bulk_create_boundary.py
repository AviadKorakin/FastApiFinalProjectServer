from typing import List
from uuid import UUID

from pydantic import BaseModel
from .user_provider_boundary import UserProviderBoundary

class UserProviderBulkCreateBoundary(BaseModel):
    provider_id: UUID
    users: List[UserProviderBoundary]
    class Config:
        from_attributes = True
