from fastapi import Depends
from repositories.sqlalchemy_person_repository import SQLAlchemyPersonRepository
from repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from repositories.user_repository import UserRepository
from services.email_service import EmailService
from services.email_service_implementation import EmailServiceImplementation
from services.person_service_implementation import PersonServiceImplementation
from services.user_service_implementation import UserServiceImplementation

def get_email_service() -> EmailServiceImplementation:
    return EmailServiceImplementation()

def get_person_repository() -> SQLAlchemyPersonRepository:
    # This will always return the same instance due to the singleton pattern
    return SQLAlchemyPersonRepository()

def get_person_service(repository: SQLAlchemyPersonRepository = Depends(get_person_repository)) -> PersonServiceImplementation:
    # This will always return the same instance due to the singleton pattern
    return PersonServiceImplementation(repository)

def get_user_repository() -> SQLAlchemyUserRepository:
    # This will always return the same instance due to the singleton pattern
    return SQLAlchemyUserRepository()

def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
    email_service: EmailService = Depends(get_email_service)
    ) -> UserServiceImplementation:
    # This will always return the same instance due to the singleton pattern
    return UserServiceImplementation(repository, email_service)