import logging
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_image_service, get_user_service
from services.image_service import ImageService
from services.user_service import UserService
from boundaries.image_boundary import ImageBoundary
from urllib.parse import unquote
import boto3
import os
from botocore.exceptions import ClientError

def get_image_router() -> APIRouter:
    router = APIRouter()

    @router.get("/presigned-url/{email}/{file_name}", response_model=str)
    async def get_presigned_url(
            email: str,
            file_name: str,
            image_service: ImageService = Depends(get_image_service),
            user_service: UserService = Depends(get_user_service),
    ):
        user = user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Generate a unique object name using a shortened UUID and date
        timestamp = datetime.utcnow().strftime('%Y%m%d')
        unique_id = uuid.uuid4().hex[:8]  # Using only the first 8 characters of the UUID
        object_name = f"{timestamp}_{unique_id}_{file_name}"

        presigned_url = image_service.generate_presigned_url(object_name=object_name)
        return presigned_url

    @router.post("/confirm-upload/{email}", response_model=ImageBoundary)
    async def confirm_upload(
            email: str,
            object_name: str,
            image_service: ImageService = Depends(get_image_service),
            user_service: UserService = Depends(get_user_service),
    ):
        user = user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
        object_name = unquote(object_name)

        s3_client = boto3.client('s3')
        try:
            s3_client.head_object(Bucket=bucket_name, Key=object_name)
        except ClientError as e:
            logging.error(
                f"Failed to find object {object_name} in bucket {bucket_name}: {e.response['Error']['Message']}")
            raise HTTPException(status_code=400,
                                detail=f"Image upload failed or URL expired: {e.response['Error']['Message']}")

        image_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        image = image_service.upload_image(object_name=object_name, url=image_url, user_email=user.email)
        return image

    @router.get("/{email}", response_model=List[ImageBoundary])
    async def list_images_for_user(
            email: str,
            page: int = 1,
            size: int = 10,
            image_service: ImageService = Depends(get_image_service),
            user_service: UserService = Depends(get_user_service),
    ):
        user = user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Implement pagination
        images = image_service.get_images_by_user(user_email=user.email, page=page, size=size)
        return images

    return router
