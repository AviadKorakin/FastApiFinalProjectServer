import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List
from app.dependencies import get_found_pet_report_service
from app.database import get_db
from boundaries.requested_found_pet_report_boundary import RequestedFoundPetReportBoundary
from boundaries.found_pet_report_boundary import FoundPetReportBoundary
from boundaries.update_found_pet_report_boundary import UpdateFoundPetReportBoundary
from services.found_pet_report_service import FoundPetReportService
from errors.validation_error import ValidationError
from errors.not_found_error import NotFoundError
from errors.database_error import DatabaseError


def get_found_pet_report_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=FoundPetReportBoundary, summary="Create Found Pet Report")
    async def create_found_pet_report(
        report_data: RequestedFoundPetReportBoundary,
        service: FoundPetReportService = Depends(get_found_pet_report_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            report = await service.create_report(
                user_id=report_data.user_id,
                geo_location=report_data.geo_location,
                description=report_data.description,
                db=db
            )
            return report
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.put("/{report_id}", response_model=FoundPetReportBoundary, summary="Update Found Pet Report")
    async def update_found_pet_report(
        report_id: uuid.UUID,
        report_data: UpdateFoundPetReportBoundary,
        service: FoundPetReportService = Depends(get_found_pet_report_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            report = await service.update_report(
                report_id=report_id,
                geo_location=report_data.geo_location,
                description=report_data.description,
                db=db
            )
            return report
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{report_id}", response_model=FoundPetReportBoundary, summary="Get Found Pet Report by ID")
    async def get_found_pet_report_by_id(
        report_id: uuid.UUID,
        service: FoundPetReportService = Depends(get_found_pet_report_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            report = await service.get_report_by_id(report_id, db)
            if not report:
                raise HTTPException(status_code=404, detail="Found Pet Report not found.")
            return report
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/", response_model=List[FoundPetReportBoundary], summary="Get All Found Pet Reports with Pagination")
    async def get_all_found_pet_reports(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        service: FoundPetReportService = Depends(get_found_pet_report_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.get_all_reports(page=page, size=size, db=db)
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/filters/", response_model=List[FoundPetReportBoundary], summary="Filter Found Pet Reports by Date, User ID, and Location")
    async def get_filtered_found_pet_reports(
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        user_id: Optional[uuid.UUID] = Query(None),
        longitude: Optional[float] = Query(None),
        latitude: Optional[float] = Query(None),
        radius_km: Optional[float] = Query(None),
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        service: FoundPetReportService = Depends(get_found_pet_report_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            reports = await service.get_reports_by_filters(
                start_date=start_date,
                end_date=end_date,
                user_id=user_id,
                longitude=longitude,
                latitude=latitude,
                radius_km=radius_km,
                page=page,
                size=size,
                db=db
            )
            return reports
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
