from abc import ABC, abstractmethod
from typing import List
from entities.user_entity import UserEntity

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> List[UserEntity]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity | None:
        pass

    @abstractmethod
    def update(self, user: UserEntity) -> UserEntity:
        pass