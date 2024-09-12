from uuid import UUID

from pydantic import BaseModel
from boundaries.user_provider_boundary import UserProviderBoundary

class UserProviderCreateBoundary(BaseModel):
    provider_id: UUID  # The provider ID
    user_provider: UserProviderBoundary  # Nested UserProviderBoundary
    class Config:
        from_attributes = True
