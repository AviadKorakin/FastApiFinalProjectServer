from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.orm import Session
from entities.person_entity import Person

class PersonRepository(ABC):
    @abstractmethod
    def create(self, person: Person) -> Person:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> list[Person]:
        pass

    @abstractmethod
    def get_by_id(self, person_id: int) -> Person | None:
        pass
