from typing import List
from entities.person_entity import Person
from repositories.person_repository import PersonRepository
from services.person_service import PersonService

class PersonServiceImplementation(PersonService):
    _instance = None

    def __new__(cls, repository: PersonRepository):
        if cls._instance is None:
            cls._instance = super(PersonServiceImplementation, cls).__new__(cls)
            cls._instance.repository = repository
        return cls._instance

    def create_person(self, first_name: str, last_name: str, age: int) -> Person:
        if age < 0 or age > 100:
            raise ValueError("Age must be a positive integer between 0 and 100")
        person = Person(first_name=first_name, last_name=last_name, age=age)
        return self.repository.create(person)

    def get_persons(self, page: int = 1, size: int = 10) -> List[Person]:
        if page < 1 or size < 1:
            raise ValueError("Page and size must be positive integers")
        skip = (page - 1) * size
        return self.repository.get_all(skip=skip, limit=size)

    def get_person_by_id(self, person_id: int) -> Person | None:
        return self.repository.get_by_id(person_id)
