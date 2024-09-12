from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import time
from uuid import UUID

from app.database import get_db
from app.dependencies import get_service_provider_service
from boundaries.service_provider_boundary import ServiceProviderBoundary
from services.service_provider_service import ServiceProviderService
from boundaries.service_provider_create_boundary import ServiceProviderCreateBoundary
from dto.service_provider_dto import ServiceProviderDTO
from dto.open_service_provider_dto import OpenServiceProviderDTO
from errors.validation_error import ValidationError
from errors.database_error import DatabaseError


def get_service_provider_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=ServiceProviderBoundary, summary="Create Service Provider")
    async def create_service_provider(
        create_boundary: ServiceProviderCreateBoundary,
        service: ServiceProviderService = Depends(get_service_provider_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            provider = await service.create_service_provider(create_boundary, db)
            return provider
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.put("/{provider_id}", response_model=ServiceProviderDTO, summary="Update Service Provider")
    async def update_service_provider(
        provider_id: UUID,
        name: Optional[str] = None,
        service_type: Optional[str] = None,
        email: Optional[str] = None,
        service: ServiceProviderService = Depends(get_service_provider_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            provider = await service.update_service_provider(
                provider_id=provider_id,  # Convert UUID to string
                name=name,
                service_type=service_type,
                email=email,
                db=db
            )
            return provider
        except ValidationError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/", response_model=List[ServiceProviderDTO], summary="Get Service Providers by Filters with Pagination")
    async def get_service_providers(
        provider_id: Optional[UUID] = None,
        user_id: Optional[UUID] = None,
        service_type: Optional[str] = None,
        name: Optional[str] = None,
        phone_number: Optional[str] = None,
        day_of_week: Optional[str] = None,
        desired_time: Optional[time] = None,
        membership: Optional[str] = None,
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        radius_km: Optional[float] = None,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        service: ServiceProviderService = Depends(get_service_provider_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            providers = await service.get_service_providers(
                provider_id=str(provider_id) if provider_id else None,
                user_id=str(user_id) if user_id else None,
                service_type=service_type,
                name=name,
                phone_number=phone_number,
                day_of_week=day_of_week,
                desired_time=desired_time,
                membership=membership,
                longitude=longitude,
                latitude=latitude,
                radius_km=radius_km,
                page=page,
                size=size,
                db=db
            )
            return providers
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/open-in", response_model=List[OpenServiceProviderDTO], summary="Get Open Service Providers for Specific Day and Time")
    async def get_open_service_providers(
        day_of_week: str,
        desired_time: time,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        service: ServiceProviderService = Depends(get_service_provider_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            providers = await service.get_open_service_providers(
                day_of_week=day_of_week,
                desired_time=desired_time,
                page=page,
                size=size,
                db=db
            )
            return providers
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
