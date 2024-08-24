from sqlalchemy.orm import Session
from typing import Type
from entities.person_entity import Person
from repositories.person_repository import PersonRepository
from utils.logging_decorator import log_db_operation
from app.database import get_db


class SQLAlchemyPersonRepository(PersonRepository):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SQLAlchemyPersonRepository, cls).__new__(cls)
        return cls._instance

    def _get_session(self) -> Session:
        """Helper method to get a new session from the get_db function."""
        db_gen = get_db()  # This is a generator
        return next(db_gen)

    @log_db_operation
    def create(self, person: Person) -> Person:
        session = self._get_session()
        try:
            session.add(person)
            session.commit()
            session.refresh(person)
            return person
        finally:
            session.close()

    @log_db_operation
    def get_all(self, skip: int = 0, limit: int = 10) -> list[Type[Person]]:
        session = self._get_session()
        try:
            return session.query(Person).offset(skip).limit(limit).all()
        finally:
            session.close()

    @log_db_operation
    def get_by_id(self, person_id: int) -> Person | None:
        session = self._get_session()
        try:
            return session.query(Person).filter(Person.id == person_id).first()
        finally:
            session.close()
