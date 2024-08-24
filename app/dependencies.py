from fastapi import Depends
from repositories.sqlalchemy_person_repository import SQLAlchemyPersonRepository
from services.person_service_implementation import PersonServiceImplementation

def get_person_repository() -> SQLAlchemyPersonRepository:
    # This will always return the same instance due to the singleton pattern
    return SQLAlchemyPersonRepository()

def get_person_service(repository: SQLAlchemyPersonRepository = Depends(get_person_repository)) -> PersonServiceImplementation:
    # This will always return the same instance due to the singleton pattern
    return PersonServiceImplementation(repository)
