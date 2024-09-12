from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.dependencies import get_working_hours_service
from boundaries.working_hours_bulk_create_boundary import WorkingHoursBulkCreateBoundary
from boundaries.working_hours_create_boundary import WorkingHoursCreateBoundary
from boundaries.working_hours_response_boundary import WorkingHoursResponseBoundary
from boundaries.working_hours_update_boundary import WorkingHoursUpdateBoundary
from services.working_hours_service import WorkingHoursService
from errors.database_error import DatabaseError
from errors.validation_error import ValidationError
from errors.not_found_error import NotFoundError
import uuid  # Import UUID

def get_working_hours_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=WorkingHoursResponseBoundary, summary="Add Working Hours")
    async def add_working_hours(
        working_hours: WorkingHoursCreateBoundary,
        service: WorkingHoursService = Depends(get_working_hours_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.add_working_hours(working_hours.provider_id, working_hours, db)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/bulk", response_model=List[WorkingHoursResponseBoundary], summary="Add Working Hours in Bulk")
    async def add_working_hours_bulk(
        bulk_boundary: WorkingHoursBulkCreateBoundary,
        service: WorkingHoursService = Depends(get_working_hours_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:

            return await service.add_working_hours_bulk(bulk_boundary.provider_id, bulk_boundary.working_hours_list, db)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.put("/", response_model=WorkingHoursResponseBoundary, summary="Update Working Hours")
    async def update_working_hours(
        working_hours: WorkingHoursUpdateBoundary,
        service: WorkingHoursService = Depends(get_working_hours_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.update_working_hours(working_hours, db)
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.delete("/{working_hours_id}", summary="Remove Working Hours")
    async def remove_working_hours(
        working_hours_id: uuid.UUID,
        service: WorkingHoursService = Depends(get_working_hours_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            await service.remove_working_hours(working_hours_id, db)
            return {"message": "Working hours removed successfully"}
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/provider/{provider_id}", response_model=List[WorkingHoursResponseBoundary], summary="Get Working Hours by Provider ID")
    async def get_working_hours_by_provider(
        provider_id: uuid.UUID,
        skip: int = 0,
        limit: int = 10,
        service: WorkingHoursService = Depends(get_working_hours_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.get_by_provider_id(provider_id, db, skip, limit)
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching working hours: {str(e)}")

    return router
