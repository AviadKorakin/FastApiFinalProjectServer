from typing import List
from entities.image_entity import ImageEntity
from repositories.image_repository import ImageRepository
import boto3
from botocore.exceptions import NoCredentialsError
from services.image_service import ImageService

class ImageServiceImplementation(ImageService):
    def __init__(self, repository: ImageRepository, s3_client: boto3.client, bucket_name: str):
        self.repository = repository
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def generate_presigned_url(self, object_name: str, expiration: int = 3600):
        try:
            response = self.s3_client.generate_presigned_url('put_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
        except NoCredentialsError:
            raise Exception("Credentials not available")
        return response

    def generate_presigned_get_url(self, object_name: str, expiration: int = 3600):
        try:
            response = self.s3_client.generate_presigned_url('get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
        except NoCredentialsError:
            raise Exception("Credentials not available")
        return response

    def upload_image(self, object_name: str, url: str, user_email: str) -> ImageEntity:
        image = ImageEntity(id=object_name, url=url, user_email=user_email)
        return self.repository.create(image)

    def get_images_by_user(self, user_email: str, page: int, size: int) -> List[ImageEntity]:
        images = self.repository.get_all_by_user_email(user_email, skip=(page - 1) * size, limit=size)
        return images
