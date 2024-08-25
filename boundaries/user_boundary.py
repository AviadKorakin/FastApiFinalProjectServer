from typing import Optional
from pydantic import BaseModel, EmailStr
from enums.role_enum import RoleEnum

class UserBoundary(BaseModel):
    email: EmailStr
    role: RoleEnum
    username: str
    avatar: Optional[str] = None

    class Config:
        orm_mode = True

