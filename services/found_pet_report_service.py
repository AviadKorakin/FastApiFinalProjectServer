from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from entities.found_pet_report_entity import FoundPetReportEntity
from boundaries.requested_found_pet_report_boundary import Location

class FoundPetReportService(ABC):

    @abstractmethod
    async def create_report(self, user_id: UUID, geo_location: Optional[Location], description: str, db: AsyncSession) -> FoundPetReportEntity:
        pass

    @abstractmethod
    async def update_report(self, report_id: UUID, geo_location: Optional[Location], description: str, db: AsyncSession) -> FoundPetReportEntity:
        pass

    @abstractmethod
    async def get_reports_by_filters(self, start_date: Optional[datetime], end_date: Optional[datetime],
                                     user_id: Optional[UUID], longitude: Optional[float], latitude: Optional[float],
                                     radius_km: Optional[float], page: int, size: int, db: AsyncSession) -> List[FoundPetReportEntity]:
        pass

    @abstractmethod
    async def get_all_reports(self, page: int, size: int, db: AsyncSession) -> List[FoundPetReportEntity]:
        pass

    @abstractmethod
    async def get_report_by_id(self, report_id: UUID, db: AsyncSession) -> Optional[FoundPetReportEntity]:
        pass
