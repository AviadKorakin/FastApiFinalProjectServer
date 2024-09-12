from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid
from entities.working_hours_entity import WorkingHoursEntity

class WorkingHoursRepository(ABC):
    @abstractmethod
    async def add_working_hours(self, working_hours: WorkingHoursEntity, db: AsyncSession) -> WorkingHoursEntity:
        """
        Inserts a new working hours entry into the database.
        :param working_hours: The WorkingHoursEntity object representing the new working hours.
        :param db: Async database session.
        :return: The created WorkingHoursEntity.
        """
        pass

    @abstractmethod
    async def add_working_hours_bulk(self, working_hours: List[WorkingHoursEntity], db: AsyncSession) -> List[WorkingHoursEntity]:
        """
        Inserts multiple working hours entries into the database in bulk.
        :param working_hours: A list of WorkingHoursEntity objects representing the new working hours.
        :param db: Async database session.
        :return: A list of created WorkingHoursEntity objects.
        """
        pass

    @abstractmethod
    async def update_working_hours(self, working_hours: WorkingHoursEntity, db: AsyncSession) -> WorkingHoursEntity:
        """
        Updates an existing working hours entry in the database.
        :param working_hours: The WorkingHoursEntity object representing the updated working hours.
        :param db: Async database session.
        :return: The updated WorkingHoursEntity.
        """
        pass

    @abstractmethod
    async def remove_working_hours(self, working_hours_id: uuid.UUID, db: AsyncSession) -> None:
        """
        Removes a working hours entry from the database by ID.
        :param working_hours_id: The UUID of the working hours to remove.
        :param db: Async database session.
        :return: None.
        """
        pass

    @abstractmethod
    async def get_by_id(self, working_hours_id: uuid.UUID, db: AsyncSession) -> Optional[WorkingHoursEntity]:
        """
        Fetches a working hours entry by ID.
        :param working_hours_id: The UUID of the working hours entry to retrieve.
        :param db: Async database session.
        :return: The WorkingHoursEntity if found, otherwise None.
        """
        pass

    @abstractmethod
    async def get_by_provider_id(self, provider_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[WorkingHoursEntity]:
        """
        Fetches working hours for a provider by their UUID with pagination.
        :param provider_id: The UUID of the service provider.
        :param db: Async database session.
        :param skip: The number of entries to skip for pagination.
        :param limit: The maximum number of entries to return.
        :return: A list of WorkingHoursEntity objects for the provider.
        """
        pass
