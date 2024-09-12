from abc import ABC, abstractmethod
from typing import List
from entities.image_entity import ImageEntity

class ImageService(ABC):
    @abstractmethod
    def generate_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        pass

    @abstractmethod
    def generate_presigned_get_url(self, object_name: str, expiration: int = 3600)-> str:
        pass
    @abstractmethod
    def upload_image(self, object_name:str, url: str, user_email: str) -> ImageEntity:
        pass

    @abstractmethod
    def get_images_by_user(self, user_email: str, page: int, size: int) -> List[ImageEntity]:
        pass
