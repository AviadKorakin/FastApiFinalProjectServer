from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from entities.pet_entity import PetEntity
from typing import List
from datetime import date
import uuid


class PetService(ABC):
    """
    Interface for the PetService. Defines all operations related to pets.
    """

    @abstractmethod
    async def create_pet(self, user_id: uuid.UUID, name: str, species: str, breed: str, date_of_birth: date,
                         main_color: str, pet_details: dict, db: AsyncSession) -> PetEntity:
        """
        Creates a new pet for a user.

        :param user_id: The UUID of the user who owns the pet.
        :param name: The name of the pet.
        :param species: The species of the pet.
        :param breed: The breed of the pet (optional).
        :param date_of_birth: The date of birth of the pet (optional).
        :param main_color: The main color of the pet (optional).
        :param pet_details: Additional details about the pet in dictionary format (optional).
        :param db: AsyncSession object for interacting with the database.
        :return: The newly created PetEntity.
        """
        pass

    @abstractmethod
    async def update_pet(self, pet_id: uuid.UUID, name: str, species: str, breed: str, date_of_birth: date,
                         main_color: str, pet_details: dict, db: AsyncSession) -> PetEntity:
        """
        Updates an existing pet's details.

        :param pet_id: The UUID of the pet to be updated.
        :param name: The updated name of the pet.
        :param species: The updated species of the pet.
        :param breed: The updated breed of the pet (optional).
        :param date_of_birth: The updated date of birth of the pet (optional).
        :param main_color: The updated main color of the pet (optional).
        :param pet_details: Additional updated details about the pet in dictionary format (optional).
        :param db: AsyncSession object for interacting with the database.
        :return: The updated PetEntity.
        """
        pass

    @abstractmethod
    async def get_pet_by_id(self, pet_id: uuid.UUID, db: AsyncSession) -> PetEntity | None:
        """
        Fetches a pet by its UUID.

        :param pet_id: The UUID of the pet to be fetched.
        :param db: AsyncSession object for interacting with the database.
        :return: The PetEntity if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_all_pets(self, page: int, size: int, db: AsyncSession) -> List[PetEntity]:
        """
        Fetches all pets with pagination.

        :param page: The page number for pagination.
        :param size: The number of pets per page.
        :param db: AsyncSession object for interacting with the database.
        :return: A list of PetEntity objects.
        """
        pass

    @abstractmethod
    async def get_pets_by_user_id(self, user_id: uuid.UUID, page: int, size: int, db: AsyncSession) -> List[PetEntity]:
        """
        Fetches all pets owned by a specific user, with pagination.

        :param user_id: The UUID of the user whose pets should be fetched.
        :param page: The page number for pagination.
        :param size: The number of pets per page.
        :param db: AsyncSession object for interacting with the database.
        :return: A list of PetEntity objects owned by the user.
        """
        pass
