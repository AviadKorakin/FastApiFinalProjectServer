from pydantic import BaseModel
from datetime import datetime

class AvatarImageBoundary(BaseModel):
    s3_file_path: str  # The full S3 path (Primary Key)
    folder_file_path: str  # The file path inside the folder (unique)
    url: str  # The S3 URL for the avatar image
    user_id: str  # The email or ID of the user
    created_at: datetime  # The timestamp when the image was created

    class Config:
        from_attributes = True  # Pydantic v2 attribute for ORM compatibility
