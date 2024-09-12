from pydantic import BaseModel

class ImageBoundary(BaseModel):
    id: str  # Assuming the ID will be the S3 object key or a generated UUID
    url: str
    user_email: str

    class Config:
        orm_mode = True
