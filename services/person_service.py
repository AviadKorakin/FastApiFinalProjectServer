from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from entities.person_entity import Person

class PersonService(ABC):
    @abstractmethod
    def create_person(self, first_name: str, last_name: str, age: int) -> Person:
        pass

    @abstractmethod
    def get_persons(self, page: int = 1, size: int = 10) -> List[Person]:
        pass

    @abstractmethod
    def get_person_by_id(self, person_id: int) -> Person | None:
        pass
