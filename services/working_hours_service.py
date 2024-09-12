from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from boundaries.working_hours_boundary import WorkingHoursBoundary
from entities.working_hours_entity import WorkingHoursEntity
from boundaries.working_hours_create_boundary import WorkingHoursCreateBoundary
from boundaries.working_hours_update_boundary import WorkingHoursUpdateBoundary

class WorkingHoursService(ABC):
    @abstractmethod
    async def add_working_hours(self, provider_id: uuid.UUID, working_hours_boundary: WorkingHoursCreateBoundary, db: AsyncSession) -> WorkingHoursEntity:
        """
        Adds new working hours for a service provider.
        :param provider_id: The UUID of the service provider.
        :param working_hours_boundary: Boundary object containing working hours data.
        :param db: Async database session.
        :return: The created WorkingHoursEntity.
        """
        pass

    @abstractmethod
    async def add_working_hours_bulk(self, provider_id: uuid.UUID, working_hours_list: List[WorkingHoursBoundary], db: AsyncSession) -> List[WorkingHoursEntity]:
        """
        Adds multiple working hours entries in bulk for a service provider.
        :param provider_id: The UUID of the service provider.
        :param working_hours_list: List of working hours boundary objects.
        :param db: Async database session.
        :return: A list of created WorkingHoursEntity objects.
        """
        pass

    @abstractmethod
    async def update_working_hours(self, working_hours_update: WorkingHoursUpdateBoundary, db: AsyncSession) -> WorkingHoursEntity:
        """
        Updates an existing working hours entry.
        :param working_hours_update: Boundary object containing updated working hours data.
        :param db: Async database session.
        :return: The updated WorkingHoursEntity.
        """
        pass

    @abstractmethod
    async def remove_working_hours(self, working_hours_id: uuid.UUID, db: AsyncSession) -> None:
        """
        Removes a working hours entry by ID.
        :param working_hours_id: The UUID of the working hours to remove.
        :param db: Async database session.
        :return: None.
        """
        pass

    @abstractmethod
    async def get_by_provider_id(self, provider_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[WorkingHoursEntity]:
        """
        Fetches working hours for a specific provider with pagination.
        :param provider_id: The UUID of the service provider.
        :param db: Async database session.
        :param skip: The number of entries to skip for pagination.
        :param limit: The maximum number of entries to return.
        :return: A list of WorkingHoursEntity objects.
        """
        pass
