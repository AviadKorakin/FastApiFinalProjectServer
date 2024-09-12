import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from entities.avatar_image_entity import AvatarImageEntity
from repositories.avatar_image_repository import AvatarImageRepository
from services.avatar_image_service import AvatarImageService
from errors.database_error import DatabaseError
from errors.validation_error import ValidationError
import uuid


class AvatarImageServiceImplementation(AvatarImageService):
    def __init__(self, repository: AvatarImageRepository, s3_client: boto3.client, bucket_name: str):
        self.repository = repository
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def generate_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        """Generate a presigned URL for image upload, enforcing JPEG content type"""
        try:
            response = self.s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name,
                    'ContentType': 'image/jpeg'  # Enforce JPEG content type
                },
                ExpiresIn=expiration
            )
            return response
        except NoCredentialsError:
            raise ValidationError("AWS credentials not available")
        except ClientError as e:
            error_message = e.response['Error']['Message']
            raise ValidationError(f"Failed to generate presigned URL: {error_message}")

    async def upload_image(self, file_path: str, s3_path: str, user_id: uuid.UUID, db: AsyncSession) -> AvatarImageEntity:
        """
        Confirm avatar image upload: Store the metadata in the database.
        The file_path is the clean file name, while s3_path includes the folder name.
        """
        try:
            # Check if the file exists in S3 (no need to validate the content type again)
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_path)
        except ClientError as e:
            error_message = e.response['Error']['Message']
            raise ValidationError(f"Failed to confirm uploaded image. Error: {error_message}")

        # Store the image metadata in the database
        image = AvatarImageEntity(
            s3_file_path=s3_path,  # Full path with the folder name
            folder_file_path=file_path,  # Clean file name without the folder
            user_id=user_id,
            url=f"https://{self.bucket_name}.s3.amazonaws.com/{s3_path}"  # Full S3 URL
        )

        try:
            avatar_image = await self.repository.create(image, db)
            await db.commit()  # Commit the transaction in the service layer
            return avatar_image
        except IntegrityError as e:
            await db.rollback()  # Rollback transaction if there's an error
            error_message = str(e.orig)
            raise DatabaseError(f"Failed to upload avatar image: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()  # Rollback transaction on database error
            raise DatabaseError(f"Unexpected database error occurred: {str(e)}")

    async def get_images_by_user(self, user_id: uuid.UUID, page: int, size: int, db: AsyncSession) -> List[AvatarImageEntity]:
        """Retrieve all avatar images for a user with pagination."""
        skip = (page - 1) * size
        try:
            return await self.repository.get_all_by_user_id(user_id=user_id, skip=skip, limit=size, db=db)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch images for user {user_id}: {str(e)}")
