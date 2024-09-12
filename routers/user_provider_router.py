import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database import get_db
from app.dependencies import get_user_provider_service
from boundaries.user_provider_create_boundary import UserProviderCreateBoundary
from boundaries.user_provider_bulk_create_boundary import UserProviderBulkCreateBoundary
from boundaries.user_provider_response_boundary import UserProviderResponseBoundary
from services.user_provider_service import UserProviderService
from errors.validation_error import ValidationError
from errors.database_error import DatabaseError

def get_user_provider_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=UserProviderResponseBoundary, summary="Add User-Provider Association")
    async def add_user_provider(
        create_boundary: UserProviderCreateBoundary,
        service: UserProviderService = Depends(get_user_provider_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.add_user_provider(
                boundary=create_boundary.user_provider,
                provider_id=create_boundary.provider_id,
                db=db
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/bulk", response_model=List[UserProviderResponseBoundary], summary="Add User-Provider Associations in Bulk")
    async def add_user_providers_bulk(
        bulk_boundary: UserProviderBulkCreateBoundary,
        service: UserProviderService = Depends(get_user_provider_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.add_user_providers_bulk(
                users=bulk_boundary.users,
                provider_id=bulk_boundary.provider_id,
                db=db
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.delete("/", summary="Remove User-Provider Association")
    async def remove_user_provider(
        user_email: str,
        provider_id: uuid.UUID,
        service: UserProviderService = Depends(get_user_provider_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            await service.remove_user_provider(user_email, provider_id, db)
            return {"message": "User-provider association removed successfully"}
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/", response_model=List[UserProviderResponseBoundary], summary="Get User-Provider Associations by Filters")
    async def get_user_providers(
        user_email: Optional[str] = None,
        provider_id: Optional[uuid.UUID] = None,
        role: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
        service: UserProviderService = Depends(get_user_provider_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.get_user_providers(user_email, provider_id, role, db, skip, limit)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
