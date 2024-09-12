import uuid
from typing import Optional, List
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.elements import WKBElement
from shapely import wkb
from entities.found_pet_report_entity import FoundPetReportEntity
from repositories.found_pet_report_repository import FoundPetReportRepository
from services.found_pet_report_service import FoundPetReportService
from boundaries.requested_found_pet_report_boundary import Location
from errors.database_error import DatabaseError
from errors.validation_error import ValidationError
from errors.not_found_error import NotFoundError


class FoundPetReportServiceImplementation(FoundPetReportService):

    def __init__(self, repository: FoundPetReportRepository):
        self.repository = repository

    async def _convert_geo_location(self, report: FoundPetReportEntity) -> None:
        """Convert WKBElement geo_location to Location object."""
        if isinstance(report.geo_location, WKBElement):
            point = wkb.loads(bytes(report.geo_location.data))
            report.geo_location = Location(latitude=point.y, longitude=point.x)  # Convert to Location object

    async def create_report(self, user_id: uuid.UUID, geo_location: Optional[Location], description: str, db: AsyncSession) -> FoundPetReportEntity:
        report = FoundPetReportEntity(
            user_id=user_id,
            geo_location=geo_location,
            description=description
        )
        try:
            created_report = await self.repository.create(report, db)
            await db.commit()
            await self._convert_geo_location(created_report)  # Conversion is done here
            return created_report
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "foreign key constraint" in error_message:
                raise ValidationError("User does not exist.")
            raise DatabaseError(f"Failed to create report due to a database error: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred: {str(e)}")

    async def update_report(self, report_id: uuid.UUID, geo_location: Optional[Location], description: str, db: AsyncSession) -> FoundPetReportEntity:
        report = await self.repository.get_by_id(report_id, db)
        if not report:
            raise NotFoundError("Found pet report not found")

        # Check for updates
        has_updates = False
        if geo_location and (geo_location.longitude != report.geo_location.longitude or geo_location.latitude != report.geo_location.latitude):
            report.geo_location = (geo_location.longitude, geo_location.latitude)
            has_updates = True
        if description and description != report.description:
            report.description = description
            has_updates = True

        if not has_updates:
            await self._convert_geo_location(report)  # Convert the geo-location to Location object before returning
            return report

        try:
            updated_report = await self.repository.update(report, db)
            await db.commit()
            await self._convert_geo_location(updated_report)  # Conversion is done here
            return updated_report
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            raise DatabaseError(f"Failed to update report due to a database constraint: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred: {str(e)}")

    async def get_reports_by_filters(self, start_date: Optional[datetime], end_date: Optional[datetime],
                                     user_id: Optional[uuid.UUID], longitude: Optional[float], latitude: Optional[float],
                                     radius_km: Optional[float], page: int, size: int, db: AsyncSession) -> List[FoundPetReportEntity]:
        try:
            skip = (page - 1) * size
            reports = await self.repository.get_reports_by_filters(start_date, end_date, user_id, longitude,
                                                                   latitude, radius_km, skip=skip, limit=size, db=db)
            for report in reports:
                await self._convert_geo_location(report)  # Convert geo-location for each report
            return reports
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch reports: {str(e)}")

    async def get_all_reports(self, page: int, size: int, db: AsyncSession) -> List[FoundPetReportEntity]:
        try:
            skip = (page - 1) * size
            reports = await self.repository.get_all(skip=skip, limit=size, db=db)
            for report in reports:
                await self._convert_geo_location(report)  # Convert geo-location for each report
            return reports
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch all reports: {str(e)}")

    async def get_report_by_id(self, report_id: uuid.UUID, db: AsyncSession) -> Optional[FoundPetReportEntity]:
        try:
            report = await self.repository.get_by_id(report_id, db)
            if report:
                await self._convert_geo_location(report)  # Conversion is done here
                return report
            raise NotFoundError("Found pet report not found")
        except SQLAlchemyError as e:
            raise DatabaseError(f"Failed to fetch report: {str(e)}")
