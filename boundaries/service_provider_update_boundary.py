from typing import Optional
from pydantic import BaseModel, EmailStr

class ServiceProviderUpdateBoundary(BaseModel):
    name: Optional[str]
    service_type: Optional[str]
    email: Optional[EmailStr]

    class Config:
        from_attributes = True
