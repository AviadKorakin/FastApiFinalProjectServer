from abc import ABC, abstractmethod
from typing import List
from entities.image_entity import ImageEntity

class ImageRepository(ABC):
    @abstractmethod
    def create(self, image: ImageEntity) -> ImageEntity:
        pass

    @abstractmethod
    def get_all_by_user_email(self, user_email: str, skip: int = 0, limit: int = 10) -> list[ImageEntity]:
        pass
