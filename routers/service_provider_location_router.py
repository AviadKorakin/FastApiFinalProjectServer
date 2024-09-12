from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.database import get_db
from app.dependencies import get_service_provider_location_service
from boundaries.service_provider_location_create_boundary import ServiceProviderLocationCreateBoundary
from boundaries.service_provider_location_bulk_create_boundary import ServiceProviderLocationBulkCreateBoundary
from boundaries.service_provider_location_response_boundary import ServiceProviderLocationResponseBoundary
from services.service_provider_location_service import ServiceProviderLocationService
from errors.database_error import DatabaseError
from errors.validation_error import ValidationError

def get_service_provider_location_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=ServiceProviderLocationResponseBoundary, summary="Add Location")
    async def add_location(
        location_boundary: ServiceProviderLocationCreateBoundary,
        service: ServiceProviderLocationService = Depends(get_service_provider_location_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            location = await service.add_location(location_boundary, db)
            return location
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/bulk", response_model=List[ServiceProviderLocationResponseBoundary], summary="Add Locations in Bulk")
    async def add_locations_bulk(
        bulk_boundary: ServiceProviderLocationBulkCreateBoundary,
        service: ServiceProviderLocationService = Depends(get_service_provider_location_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            locations = await service.add_locations_bulk(bulk_boundary.locations, db)
            return locations
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.delete("/{location_id}", summary="Remove Location")
    async def remove_location(
        location_id: uuid.UUID,
        service: ServiceProviderLocationService = Depends(get_service_provider_location_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            await service.remove_location(location_id, db)
            return {"message": "Location removed successfully"}
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{provider_id}", response_model=List[ServiceProviderLocationResponseBoundary], summary="Get Locations by Provider")
    async def get_locations_by_provider_id(
        provider_id: uuid.UUID,
        skip: int = 0,
        limit: int = 10,
        service: ServiceProviderLocationService = Depends(get_service_provider_location_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            locations = await service.get_locations_by_provider_id(provider_id, db, skip, limit)
            return locations
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/", response_model=List[ServiceProviderLocationResponseBoundary], summary="Get All Locations with Pagination")
    async def get_all_locations(
        skip: int = 0,
        limit: int = 10,
        service: ServiceProviderLocationService = Depends(get_service_provider_location_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            locations = await service.get_all_locations(db, skip, limit)
            return locations
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
