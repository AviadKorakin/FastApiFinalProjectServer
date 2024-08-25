from typing import List
from entities.user_entity import UserEntity
from enums.role_enum import RoleEnum
from repositories.user_repository import UserRepository
from services.email_service import EmailService
from services.user_service import UserService
from passlib.context import CryptContext
import secrets
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserServiceImplementation(UserService):
    _instance = None

    def __new__(cls, repository: UserRepository, email_service: EmailService):
        if cls._instance is None:
            cls._instance = super(UserServiceImplementation, cls).__new__(cls)
            cls._instance.repository = repository
            cls._instance.email_service = email_service
        return cls._instance

    def create_user(self, email: str, password: str, role: str, username: str, avatar: str = None,
                    verification_url: str = None) -> UserEntity:
        existing_user = self.repository.get_by_email(email)
        if existing_user:
            raise ValueError("A user with this email already exists.")

        hashed_password = self._hash_password(password)
        role_enum = RoleEnum[role.upper()]
        token = secrets.token_urlsafe(16)  # Generate a secure token
        expiration = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour

        user = UserEntity(
            email=email,
            hashed_password=hashed_password,
            role=role_enum,
            username=username,
            avatar=avatar,
            verification_token=token,
            token_expiration=expiration
        )

        # Replace the placeholder in the verification URL with the actual token
        verification_url = verification_url.replace('{token}', token)

        # Send the verification email with the provided URL
        self.email_service.send_verification_email(email, verification_url)
        return self.repository.create(user)


    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def login_user(self, email: str, password: str) -> UserEntity | None:
        user = self.repository.get_by_email(email)
        if user and self.verify_password(password, user.hashed_password):
            if not user.email_verified:
                raise ValueError("Email not verified.")
            return user
        raise ValueError("Invalid email or password.")

    def verify_email(self, email: str, token: str) -> bool:
        user = self.repository.get_by_email(email)
        if user and user.verification_token == token and datetime.utcnow() <= user.token_expiration:
            user.email_verified = True
            user.verification_token = None
            user.token_expiration = None
            self.repository.update(user)  # Save changes to the database
            return True
        return False

    def get_users(self, page: int = 1, size: int = 10) -> List[UserEntity]:
        if page < 1 or size < 1:
            raise ValueError("Page and size must be positive integers")
        skip = (page - 1) * size
        return self.repository.get_all(skip=skip, limit=size)

    def get_user_by_email(self, email: str) -> UserEntity | None:
        return self.repository.get_by_email(email)
