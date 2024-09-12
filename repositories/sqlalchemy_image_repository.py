from sqlalchemy.orm import Session
from typing import List, Type
from app.database import get_db
from entities.image_entity import ImageEntity
from repositories.image_repository import ImageRepository

class SQLAlchemyImageRepository(ImageRepository):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SQLAlchemyImageRepository, cls).__new__(cls)
        return cls._instance

    def _get_session(self) -> Session:
        db_gen = get_db()
        return next(db_gen)

    def create(self, image: ImageEntity) -> ImageEntity:
        session = self._get_session()
        try:
            session.add(image)
            session.commit()
            session.refresh(image)
            return image
        finally:
            session.close()

    def get_all_by_user_email(self, user_email: str, skip: int = 0, limit: int = 10) -> list[Type[ImageEntity]]:
        session = self._get_session()
        try:
            return session.query(ImageEntity).filter(ImageEntity.user_email == user_email).offset(skip).limit(limit).all()
        finally:
            session.close()
