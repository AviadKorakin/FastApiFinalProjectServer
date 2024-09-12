import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from entities.found_pet_report_entity import FoundPetReportEntity
from repositories.found_pet_report_repository import FoundPetReportRepository
from typing import Optional, List
from datetime import datetime
from geoalchemy2 import functions as geo_funcs


class SQLAlchemyFoundPetReportRepository(FoundPetReportRepository):

    async def create(self, report: FoundPetReportEntity, db: AsyncSession) -> FoundPetReportEntity:
        db.add(report)
        await db.flush()
        await db.refresh(report)
        return report

    async def update(self, report: FoundPetReportEntity, db: AsyncSession) -> FoundPetReportEntity:
        # Handle geo-location update if applicable
        if report.geo_location:
            longitude, latitude = report.geo_location
            report.geo_location = geo_funcs.ST_SetSRID(geo_funcs.ST_MakePoint(longitude, latitude), 4326)

        await db.flush()
        await db.refresh(report)
        return report

    async def get_by_id(self, report_id: uuid.UUID, db: AsyncSession) -> Optional[FoundPetReportEntity]:
        result = await db.execute(
            select(FoundPetReportEntity).where(FoundPetReportEntity.report_id == report_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int, limit: int, db: AsyncSession) -> List[FoundPetReportEntity]:
        result = await db.execute(
            select(FoundPetReportEntity).order_by(FoundPetReportEntity.report_date.desc())
            .offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def get_reports_by_filters(self, start_date: Optional[datetime], end_date: Optional[datetime],
                                     user_id: Optional[uuid.UUID], longitude: Optional[float], latitude: Optional[float],
                                     radius_km: Optional[float], skip: int, limit: int, db: AsyncSession) -> List[
        FoundPetReportEntity]:
        query = select(FoundPetReportEntity)

        # Date range filtering
        if start_date and end_date:
            query = query.where(FoundPetReportEntity.report_date.between(start_date, end_date))
        elif start_date:
            query = query.where(FoundPetReportEntity.report_date >= start_date)
        elif end_date:
            query = query.where(FoundPetReportEntity.report_date <= end_date)

        # User ID filtering
        if user_id:
            query = query.where(FoundPetReportEntity.user_id == user_id)

        # Geo-location filtering
        if longitude is not None and latitude is not None and radius_km is not None:
            point = geo_funcs.ST_SetSRID(geo_funcs.ST_MakePoint(longitude, latitude), 4326)
            query = query.where(geo_funcs.ST_DWithin(FoundPetReportEntity.geo_location, point, radius_km * 1000))
            query = query.order_by(geo_funcs.ST_Distance(FoundPetReportEntity.geo_location, point))

        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()
