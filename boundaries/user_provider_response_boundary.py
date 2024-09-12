from uuid import UUID

from pydantic import BaseModel
from enums.user_provider_role_enum import UserProviderRoleEnum

class UserProviderResponseBoundary(BaseModel):
    user_id: UUID  # The email of the user associated with the provider
    provider_id: UUID  # The ID of the service provider
    role: UserProviderRoleEnum  # The role of the user in the provider association

    class Config:
        orm_mode = True  # Enable ORM mode to allow compatibility with SQLAlchemy models
