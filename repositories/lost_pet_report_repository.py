from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from entities.lost_pet_report_entity import LostPetReportEntity

class LostPetReportRepository(ABC):
    @abstractmethod
    async def create(self, report: LostPetReportEntity, db: AsyncSession) -> LostPetReportEntity:
        pass

    @abstractmethod
    async def update(self, report: LostPetReportEntity, db: AsyncSession) -> LostPetReportEntity:
        pass

    @abstractmethod
    async def get_by_id(self, report_id: UUID, db: AsyncSession) -> Optional[LostPetReportEntity]:
        pass

    @abstractmethod
    async def get_all(self, skip: int, limit: int, db: AsyncSession) -> List[LostPetReportEntity]:
        pass

    @abstractmethod
    async def get_reports_by_filters(self, start_date: Optional[datetime], end_date: Optional[datetime], status: Optional[str], user_id: Optional[UUID], pet_id: Optional[UUID], longitude: Optional[float], latitude: Optional[float], radius_km: Optional[float], skip: int, limit: int, db: AsyncSession) -> List[LostPetReportEntity]:
        pass
