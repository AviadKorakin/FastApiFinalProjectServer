from uuid import UUID

from pydantic import BaseModel

from enums.user_provider_role_enum import UserProviderRoleEnum


class UserProviderBoundary(BaseModel):
    user_id: UUID
    role: UserProviderRoleEnum
    class Config:
        from_attributes = True
