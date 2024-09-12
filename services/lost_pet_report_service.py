from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from entities.lost_pet_report_entity import LostPetReportEntity
from boundaries.lost_pet_report_boundary import Location

class LostPetReportService(ABC):
    @abstractmethod
    async def create_report(self, pet_id: UUID, user_id: UUID, geo_location: Optional[Location], description: str, status: str, db: AsyncSession) -> LostPetReportEntity:
        pass

    @abstractmethod
    async def update_report(self, report_id: UUID, geo_location: Optional[Location], description: str, status: str, db: AsyncSession) -> LostPetReportEntity:
        pass

    @abstractmethod
    async def get_reports_by_filters(self, start_date: Optional[datetime], end_date: Optional[datetime], status: Optional[str], user_id: Optional[UUID], pet_id: Optional[UUID], longitude: Optional[float], latitude: Optional[float], radius_km: Optional[float], page: int, size: int, db: AsyncSession) -> List[LostPetReportEntity]:
        pass

    @abstractmethod
    async def get_all_reports(self, page: int, size: int, db: AsyncSession) -> List[LostPetReportEntity]:
        pass

    @abstractmethod
    async def get_report_by_id(self, report_id: UUID, db: AsyncSession) -> Optional[LostPetReportEntity]:
        pass
