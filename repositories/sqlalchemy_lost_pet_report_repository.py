from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from entities.lost_pet_report_entity import LostPetReportEntity
from repositories.lost_pet_report_repository import LostPetReportRepository
from typing import Optional, List
from datetime import datetime
import uuid


class SQLAlchemyLostPetReportRepository(LostPetReportRepository):

    async def create(self, report: LostPetReportEntity, db: AsyncSession) -> LostPetReportEntity:
        db.add(report)
        await db.flush()
        await db.refresh(report)
        return report

    async def update(self, report: LostPetReportEntity, db: AsyncSession) -> LostPetReportEntity:
        if report.geo_location:
            longitude, latitude = report.geo_location
            geo_point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
            report.geo_location = geo_point
        await db.flush()
        await db.refresh(report)
        return report

    async def get_by_id(self, report_id: uuid.UUID, db: AsyncSession) -> Optional[LostPetReportEntity]:
        result = await db.execute(select(LostPetReportEntity).filter_by(report_id=report_id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int, limit: int, db: AsyncSession) -> List[LostPetReportEntity]:
        result = await db.execute(
            select(LostPetReportEntity).order_by(LostPetReportEntity.report_date.desc())
            .offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_reports_by_filters(self, start_date: Optional[datetime], end_date: Optional[datetime],
                                     status: Optional[str], user_id: Optional[uuid.UUID], pet_id: Optional[uuid.UUID],
                                     longitude: Optional[float], latitude: Optional[float], radius_km: Optional[float],
                                     skip: int, limit: int, db: AsyncSession) -> List[LostPetReportEntity]:
        query = select(LostPetReportEntity)

        # Apply filters
        if start_date and end_date:
            query = query.where(LostPetReportEntity.report_date.between(start_date, end_date))
        elif start_date:
            query = query.where(LostPetReportEntity.report_date >= start_date)
        elif end_date:
            query = query.where(LostPetReportEntity.report_date <= end_date)

        if status:
            query = query.where(LostPetReportEntity.status == status)

        if user_id:
            query = query.where(LostPetReportEntity.user_id == user_id)

        if pet_id:
            query = query.where(LostPetReportEntity.pet_id == pet_id)

        if longitude is not None and latitude is not None and radius_km is not None:
            point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
            query = query.where(func.ST_DWithin(LostPetReportEntity.geo_location, point, radius_km * 1000))
            query = query.order_by(func.ST_Distance(LostPetReportEntity.geo_location, point))

        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
