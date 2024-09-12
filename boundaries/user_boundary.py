from uuid import UUID

from pydantic import BaseModel,FieldValidationInfo, field_validator
from enums.role_enum import RoleEnum

class UserBoundary(BaseModel):
    user_id:UUID
    email: str
    first_name: str
    last_name: str
    phone_number: str  # No need to validate on output
    role: RoleEnum

    class Config:
        from_attributes = True
