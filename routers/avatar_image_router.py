import logging
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from urllib.parse import urlparse, unquote
import os
from typing import List
from app.dependencies import get_avatar_image_service, get_user_service
from app.database import get_db
from services.avatar_image_service import AvatarImageService
from services.user_service import UserService
from boundaries.avatar_image_boundary import AvatarImageBoundary
from errors.database_error import DatabaseError
from errors.validation_error import ValidationError


def get_avatar_image_router() -> APIRouter:
    router = APIRouter()

    @router.get("/presigned-url/{user_id}/{file_name}", response_model=str, summary="Get Presigned Upload URL")
    async def get_presigned_url(
            user_id: uuid.UUID,
            file_name: str,
            avatar_image_service: AvatarImageService = Depends(get_avatar_image_service),
            user_service: UserService = Depends(get_user_service),
            db: AsyncSession = Depends(get_db)
    ):
        user = await user_service.get_user_by_id(user_id=user_id, db=db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        timestamp = datetime.utcnow().strftime('%Y%m%d')
        unique_id = uuid.uuid4().hex[:8]
        object_name = f"AvatarImages/{timestamp}_{unique_id}_{file_name}"

        try:
            presigned_url = avatar_image_service.generate_presigned_url(object_name=object_name)
            return presigned_url
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post("/confirm-upload/{user_id}", response_model=AvatarImageBoundary, summary="Confirm Avatar Image Upload")
    async def confirm_upload(
            user_id: uuid.UUID,
            presigned_url: str,
            avatar_image_service: AvatarImageService = Depends(get_avatar_image_service),
            user_service: UserService = Depends(get_user_service),
            db: AsyncSession = Depends(get_db)
    ):
        user = await user_service.get_user_by_id(user_id=user_id, db=db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Parse the presigned URL to extract the file path
        parsed_url = urlparse(unquote(presigned_url))
        file_path = parsed_url.path.lstrip('/')  # Remove leading slash

        # Extract folder name and file name from file_path
        folder_name, file_name = os.path.split(file_path)

        s3_path = f"{folder_name}/{file_name}"  # Full S3 path with folder and file

        try:
            avatar_image = await avatar_image_service.upload_image(file_path=file_name, s3_path=s3_path, user_id=user.user_id, db=db)
            return avatar_image
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{user_id}", response_model=List[AvatarImageBoundary], summary="List Avatar Images for User")
    async def list_images_for_user(
            user_id: uuid.UUID,
            page: int = Query(1, ge=1),
            size: int = Query(10, ge=1),
            avatar_image_service: AvatarImageService = Depends(get_avatar_image_service),
            user_service: UserService = Depends(get_user_service),
            db: AsyncSession = Depends(get_db)
    ):
        user = await user_service.get_user_by_id(user_id=user_id, db=db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        try:
            images = await avatar_image_service.get_images_by_user(user_id=user.user_id, page=page, size=size, db=db)
            return images
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
