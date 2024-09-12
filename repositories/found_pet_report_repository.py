from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from uuid import UUID
from entities.found_pet_report_entity import FoundPetReportEntity

class FoundPetReportRepository(ABC):

    @abstractmethod
    async def create(self, report: FoundPetReportEntity, db: AsyncSession) -> FoundPetReportEntity:
        pass

    @abstractmethod
    async def update(self, report: FoundPetReportEntity, db: AsyncSession) -> FoundPetReportEntity:
        pass

    @abstractmethod
    async def get_by_id(self, report_id: UUID, db: AsyncSession) -> Optional[FoundPetReportEntity]:
        pass

    @abstractmethod
    async def get_all(self, skip: int, limit: int, db: AsyncSession) -> List[FoundPetReportEntity]:
        pass

    @abstractmethod
    async def get_reports_by_filters(self, start_date: Optional[datetime], end_date: Optional[datetime],
                                     user_id: Optional[UUID], longitude: Optional[float], latitude: Optional[float],
                                     radius_km: Optional[float], skip: int, limit: int,
                                     db: AsyncSession) -> List[FoundPetReportEntity]:
        pass
