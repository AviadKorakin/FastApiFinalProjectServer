# app/dependencies.py
from fastapi import Depends

from repositories.sqlalchemy_person_repository import SQLAlchemyPersonRepository
from services.person_service_implementation import PersonServiceImplementation
from services.person_service import PersonService

def get_person_repository() -> SQLAlchemyPersonRepository:
    return SQLAlchemyPersonRepository()

def get_person_service(repository: SQLAlchemyPersonRepository = Depends(get_person_repository)) -> PersonService:
    return PersonServiceImplementation(repository)
