from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.database import get_db
from app.dependencies import get_provider_phone_service
from boundaries.provider_phone_create_boundary import ProviderPhoneCreateBoundary
from boundaries.provider_phone_bulk_create_boundary import ProviderPhoneBulkCreateBoundary
from boundaries.provider_phone_response_boundary import ProviderPhoneResponseBoundary
from services.provider_phone_service import ProviderPhoneService
from errors.database_error import DatabaseError
from errors.validation_error import ValidationError

def get_provider_phone_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=ProviderPhoneResponseBoundary, summary="Add Phone Number")
    async def add_phone(
        phone_boundary: ProviderPhoneCreateBoundary,
        service: ProviderPhoneService = Depends(get_provider_phone_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            phone = await service.add_phone(phone_boundary.provider_id, phone_boundary.phone, db)
            return phone
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/bulk", response_model=List[ProviderPhoneResponseBoundary], summary="Add Phone Numbers in Bulk")
    async def add_phones_bulk(
        bulk_boundary: ProviderPhoneBulkCreateBoundary,
        service: ProviderPhoneService = Depends(get_provider_phone_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            phones = await service.add_phones_bulk(bulk_boundary.provider_id, bulk_boundary.phones, db)
            return phones
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.delete("/{phone_id}", summary="Remove Phone Number")
    async def remove_phone(
        phone_id: uuid.UUID,
        service: ProviderPhoneService = Depends(get_provider_phone_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            await service.remove_phone(phone_id, db)
            return {"message": "Phone number removed successfully"}
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{provider_id}", response_model=List[ProviderPhoneResponseBoundary], summary="Get Phones by Provider")
    async def get_phones_by_provider_id(
        provider_id: uuid.UUID,
        skip: int = 0,
        limit: int = 10,
        service: ProviderPhoneService = Depends(get_provider_phone_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            phones = await service.get_phones_by_provider_id(provider_id, db, skip, limit)
            return phones
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/", response_model=List[ProviderPhoneResponseBoundary], summary="Get All Phones with Pagination")
    async def get_all_phones(
        skip: int = 0,
        limit: int = 10,
        service: ProviderPhoneService = Depends(get_provider_phone_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            phones = await service.get_all_phones(db, skip, limit)
            return phones
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
