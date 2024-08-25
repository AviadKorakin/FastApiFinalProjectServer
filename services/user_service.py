from abc import ABC, abstractmethod
from typing import List
from entities.user_entity import UserEntity

class UserService(ABC):
    @abstractmethod
    def create_user(self, email: str, password: str, role: str, username: str, avatar: str = None,
                    verification_url: str = None) -> UserEntity:
        pass

    @abstractmethod
    def get_users(self, page: int = 1, size: int = 10) -> List[UserEntity]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserEntity | None:
        pass

    @abstractmethod
    def login_user(self, email: str, password: str) -> UserEntity | None:
        pass
    @abstractmethod
    def verify_email(self, email: str, token: str) -> bool:
        pass