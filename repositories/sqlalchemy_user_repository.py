from sqlalchemy.orm import Session
from typing import List, Type
from entities.user_entity import UserEntity
from repositories.user_repository import UserRepository
from utils.logging_decorator import log_db_operation
from app.database import get_db

class SQLAlchemyUserRepository(UserRepository):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SQLAlchemyUserRepository, cls).__new__(cls)
        return cls._instance

    def _get_session(self) -> Session:
        """Helper method to get a new session from the get_db function."""
        db_gen = get_db()  # This is a generator
        return next(db_gen)

    @log_db_operation
    def create(self, user: UserEntity) -> UserEntity:
        session = self._get_session()
        try:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()

    @log_db_operation
    def get_all(self, skip: int = 0, limit: int = 10) -> list[Type[UserEntity]]:
        session = self._get_session()
        try:
            return session.query(UserEntity).offset(skip).limit(limit).all()
        finally:
            session.close()

    @log_db_operation
    def get_by_email(self, email: str) -> UserEntity | None:
        session = self._get_session()
        try:
            return session.query(UserEntity).filter(UserEntity.email == email).first()
        finally:
            session.close()

    @log_db_operation
    def update(self, user: UserEntity) -> UserEntity:
        session = self._get_session()
        try:
            session.merge(user)
            session.commit()
            return user
        finally:
            session.close()
