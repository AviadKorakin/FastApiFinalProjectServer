import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.elements import WKBElement
from shapely import wkb
from entities.lost_pet_report_entity import LostPetReportEntity
from repositories.lost_pet_report_repository import LostPetReportRepository
from services.lost_pet_report_service import LostPetReportService
from boundaries.lost_pet_report_boundary import Location
from errors.database_error import DatabaseError
from errors.validation_error import ValidationError
from errors.not_found_error import NotFoundError


class LostPetReportServiceImplementation(LostPetReportService):

    def __init__(self, repository: LostPetReportRepository):
        self.repository = repository

    async def _convert_geo_location(self, report: LostPetReportEntity) -> LostPetReportEntity:
        if isinstance(report.geo_location, WKBElement):
            point = wkb.loads(bytes(report.geo_location.data))
            report.geo_location = Location(latitude=point.y, longitude=point.x)
        return report

    async def create_report(self, pet_id: uuid.UUID, user_id: uuid.UUID, geo_location: Optional[Location], description: str, status: str, db: AsyncSession) -> LostPetReportEntity:
        report = LostPetReportEntity(
            pet_id=pet_id,
            user_id=user_id,
            geo_location=geo_location,
            description=description,
            status=status
        )
        try:
            created_report = await self.repository.create(report, db)
            await db.commit()
            return await self._convert_geo_location(created_report)
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "foreign key constraint" in error_message:
                raise ValidationError("Pet or user does not exist.")
            raise DatabaseError(f"Failed to create report due to a database error: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred: {str(e)}")

    async def update_report(self, report_id: uuid.UUID, geo_location: Optional[Location], description: str, status: str, db: AsyncSession) -> LostPetReportEntity:
        report = await self.repository.get_by_id(report_id, db)
        if not report:
            raise NotFoundError("Lost pet report not found")

        has_updates = False
        if geo_location and geo_location != report.geo_location:
            report.geo_location = geo_location
            has_updates = True
        if description and description != report.description:
            report.description = description
            has_updates = True
        if status and status != report.status:
            report.status = status
            has_updates = True

        if not has_updates:
            return report

        try:
            updated_report = await self.repository.update(report, db)
            await db.commit()
            return await self._convert_geo_location(updated_report)
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            raise DatabaseError(f"Failed to update report due to a database constraint: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred: {str(e)}")

    async def get_reports_by_filters(self, start_date: Optional[datetime], end_date: Optional[datetime],
                                     status: Optional[str], user_id: Optional[uuid.UUID], pet_id: Optional[uuid.UUID],
                                     longitude: Optional[float], latitude: Optional[float], radius_km: Optional[float],
                                     page: int, size: int, db: AsyncSession) -> List[LostPetReportEntity]:
        try:
            skip = (page - 1) * size
            reports = await self.repository.get_reports_by_filters(
                start_date, end_date, status, user_id, pet_id, longitude, latitude, radius_km, skip=skip, limit=size, db=db
            )
            for report in reports:
                await self._convert_geo_location(report)
            return reports
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch reports: {str(e)}")

    async def get_all_reports(self, page: int, size: int, db: AsyncSession) -> List[LostPetReportEntity]:
        try:
            skip = (page - 1) * size
            reports = await self.repository.get_all(skip=skip, limit=size, db=db)
            for report in reports:
                await self._convert_geo_location(report)
            return reports
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch all reports: {str(e)}")

    async def get_report_by_id(self, report_id: uuid.UUID, db: AsyncSession) -> Optional[LostPetReportEntity]:
        try:
            report = await self.repository.get_by_id(report_id, db)
            if report:
                return await self._convert_geo_location(report)
            raise NotFoundError("Lost pet report not found")
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch report: {str(e)}")
