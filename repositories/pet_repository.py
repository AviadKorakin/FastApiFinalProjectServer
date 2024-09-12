from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from entities.pet_entity import PetEntity
from typing import List
import uuid


class PetRepository(ABC):
    """
    Interface for the PetRepository. Defines data access operations related to pets.
    """

    @abstractmethod
    async def create(self, pet: PetEntity, db: AsyncSession) -> PetEntity:
        """
        Inserts a new pet into the database.

        :param pet: The PetEntity object representing the pet to be created.
        :param db: AsyncSession object for interacting with the database.
        :return: The created PetEntity.
        """
        pass

    @abstractmethod
    async def update(self, pet: PetEntity, db: AsyncSession) -> PetEntity:
        """
        Updates an existing pet's information in the database.

        :param pet: The PetEntity object representing the pet to be updated.
        :param db: AsyncSession object for interacting with the database.
        :return: The updated PetEntity.
        """
        pass

    @abstractmethod
    async def get_by_pet_id(self, pet_id: uuid.UUID, db: AsyncSession) -> PetEntity | None:
        """
        Retrieves a pet by its UUID from the database.

        :param pet_id: The UUID of the pet to retrieve.
        :param db: AsyncSession object for interacting with the database.
        :return: The PetEntity if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_all(self, skip: int, limit: int, db: AsyncSession) -> List[PetEntity]:
        """
        Retrieves all pets from the database, with pagination.

        :param skip: The number of records to skip (used for pagination).
        :param limit: The number of records to retrieve (used for pagination).
        :param db: AsyncSession object for interacting with the database.
        :return: A list of PetEntity objects.
        """
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: uuid.UUID, skip: int, limit: int, db: AsyncSession) -> List[PetEntity]:
        """
        Retrieves all pets for a specific user from the database, with pagination.

        :param user_id: The UUID of the user whose pets should be retrieved.
        :param skip: The number of records to skip (used for pagination).
        :param limit: The number of records to retrieve (used for pagination).
        :param db: AsyncSession object for interacting with the database.
        :return: A list of PetEntity objects owned by the user.
        """
        pass
