from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List
import uuid
from app.dependencies import get_lost_pet_report_service
from app.database import get_db
from boundaries.requested_lost_pet_report_boundary import RequestedLostPetReportBoundary
from boundaries.update_lost_pet_report_boundary import UpdateLostPetReportBoundary
from services.lost_pet_report_service import LostPetReportService
from boundaries.lost_pet_report_boundary import LostPetReportBoundary
from errors.validation_error import ValidationError
from errors.not_found_error import NotFoundError
from errors.database_error import DatabaseError

def get_lost_pet_report_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=LostPetReportBoundary, summary="Create Lost Pet Report")
    async def create_lost_pet_report(
        report_data: RequestedLostPetReportBoundary,
        service: LostPetReportService = Depends(get_lost_pet_report_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            report = await service.create_report(
                pet_id=report_data.pet_id,
                user_id=report_data.user_id,
                geo_location=report_data.geo_location,
                description=report_data.description,
                status=report_data.status,
                db=db
            )
            return report
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    @router.put("/{report_id}", response_model=LostPetReportBoundary, summary="Update Lost Pet Report")
    async def update_lost_pet_report(
        report_id: uuid.UUID,
        report_data: UpdateLostPetReportBoundary,
        service: LostPetReportService = Depends(get_lost_pet_report_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            report = await service.update_report(
                report_id=report_id,
                geo_location=report_data.geo_location,
                description=report_data.description,
                status=report_data.status,
                db=db
            )
            return report
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{report_id}", response_model=LostPetReportBoundary, summary="Get Lost Pet Report by ID")
    async def get_lost_pet_report_by_id(
        report_id: uuid.UUID,
        service: LostPetReportService = Depends(get_lost_pet_report_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            report = await service.get_report_by_id(report_id, db)
            if not report:
                raise HTTPException(status_code=404, detail="Lost Pet Report not found.")
            return report
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/", response_model=List[LostPetReportBoundary], summary="Get All Lost Pet Reports with Pagination")
    async def get_all_lost_pet_reports(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        service: LostPetReportService = Depends(get_lost_pet_report_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.get_all_reports(page=page, size=size, db=db)
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    @router.get("/filters/", response_model=List[LostPetReportBoundary], summary="Filter Lost Pet Reports")
    async def get_filtered_lost_pet_reports(
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        status: Optional[str] = Query(None),
        user_id: Optional[uuid.UUID] = Query(None),
        pet_id: Optional[uuid.UUID] = Query(None),
        longitude: Optional[float] = Query(None),
        latitude: Optional[float] = Query(None),
        radius_km: Optional[float] = Query(None),
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        service: LostPetReportService = Depends(get_lost_pet_report_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            reports = await service.get_reports_by_filters(
                start_date=start_date,
                end_date=end_date,
                status=status,
                user_id=user_id,
                pet_id=pet_id,
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    return router
