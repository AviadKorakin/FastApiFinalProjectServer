import os

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from repositories.user_repository import UserRepository
from services.user_service import UserService
from entities.user_entity import UserEntity
from services.email_service import EmailService
from errors.not_found_error import NotFoundError
from errors.validation_error import ValidationError
from errors.database_error import DatabaseError
from passlib.context import CryptContext
import secrets
from datetime import datetime, timedelta, timezone
from typing import List, Optional
import uuid
from utils.jwt_helper import create_access_token
crypt_scheme = os.getenv("CRYPT_SCHEME")
pwd_context = CryptContext(schemes=[crypt_scheme], deprecated="auto")


class UserServiceImplementation(UserService):

    def __init__(self, repository: UserRepository, email_service: EmailService):
        self.repository = repository
        self.email_service = email_service

    async def create_user(self, email: str, password: str, first_name: str, last_name: str, role: str,
                          phone_number: str, db: AsyncSession = None) -> tuple[UserEntity, str]:
        hashed_password = self._hash_password(password)
        token = secrets.token_urlsafe(16)  # Generate the token
        expiration = datetime.now(timezone.utc) + timedelta(hours=1)

        user = UserEntity(
            email=email,
            first_name=first_name,
            last_name=last_name,
            hashed_password=hashed_password,
            role=role.upper(),
            phone_number=phone_number,
            verification_token=token,  # Store the token
            token_expiration=expiration  # Set token expiration time
        )

        try:
            user = await self.repository.create(user, db)
            await db.commit()

            return user, token  # Return the user and token
        except IntegrityError:
            await db.rollback()
            raise ValidationError(f"User with email {email} already exists.")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error during user creation: {str(e)}")

    async def send_verification_email(self, email: str, verification_url: str):
        # Your email service call to send the email
        await self.email_service.send_verification_email(email, verification_url)

    async def login_user(self, email: str, password: str, db: AsyncSession) -> Optional[UserEntity]:
        try:
            user = await self.repository.get_by_email(db, email)
            if user and self.verify_password(password, user.hashed_password):
                if not user.email_verified:
                    raise ValidationError("Email not verified.")
                return user
            raise NotFoundError("Invalid email or password.")
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error during login: {str(e)}")

    async def verify_email(self, user_id: uuid.UUID, token: str, db: AsyncSession) -> bool:
        try:
            user = await self.repository.get_by_id(db, user_id)
            if user and user.verification_token == token and datetime.now(timezone.utc) <= user.token_expiration:
                user.email_verified = True
                user.verification_token = None
                user.token_expiration = None
                await self.repository.update(db, user)
                await db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error during email verification: {str(e)}")

    async def reset_token(self, email: str, db: AsyncSession) -> tuple[uuid.UUID, str]:
        try:
            # Step 1: Retrieve the user by email
            user = await self.repository.get_by_email(db, email)
            if not user:
                raise NotFoundError(f"User with email {email} does not exist.")

            # Step 2: Check if the user is already verified
            if user.verification_token is None:
                raise ValidationError(f"User with email {email} is already verified.")

            # Step 3: Generate a new token and set expiration
            token = secrets.token_urlsafe(16)
            expiration = datetime.now(timezone.utc) + timedelta(hours=1)
            user.verification_token = token
            user.token_expiration = expiration

            # Step 4: Update the user in the database and commit
            await self.repository.update(db, user)
            await db.commit()

            return user.user_id, token  # Return the user ID and the generated token

        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error during token reset: {str(e)}")

    async def update_user_details(self, user_id: uuid.UUID, old_password: str, new_password: Optional[str],
                                  first_name: Optional[str], last_name: Optional[str],
                                  phone_number: Optional[str], db: AsyncSession) -> UserEntity:
        try:
            user = await self.repository.get_by_id(db, user_id)
            if not user:
                raise NotFoundError(f"User with ID '{user_id}' not found.")

            if not old_password or not self.verify_password(old_password, user.hashed_password):
                raise ValidationError("Incorrect old password.")

            # Track whether any changes are made
            changes_made = False

            # Update only if new_password is provided and different
            if new_password:
                hashed_new_password = self._hash_password(new_password)
                if hashed_new_password != user.hashed_password:
                    user.hashed_password = hashed_new_password
                    changes_made = True

            # Update first_name if it is provided and different
            if first_name is not None and first_name != user.first_name:
                user.first_name = first_name
                changes_made = True

            # Update last_name if it is provided and different
            if last_name is not None and last_name != user.last_name:
                user.last_name = last_name
                changes_made = True

            # Update phone_number if it is provided and different
            if phone_number is not None and phone_number != user.phone_number:
                user.phone_number = phone_number
                changes_made = True

            # If no changes were made, skip the database update
            if changes_made:
                updated_user = await self.repository.update_user_details(user, db)
                await db.commit()
                return updated_user
            else:
                return user  # Return the user without updating the database

        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error during user update: {str(e)}")

    async def get_users(self, db: AsyncSession, page: int = 1, size: int = 10) -> List[UserEntity]:
        skip = (page - 1) * size
        try:
            return await self.repository.get_all(db, skip=skip, limit=size)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error fetching users: {str(e)}")

    async def get_user_by_id(self, user_id: uuid.UUID, db: AsyncSession) -> Optional[UserEntity]:
        try:
            return await self.repository.get_by_id(db, user_id)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error fetching user by ID: {str(e)}")

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
