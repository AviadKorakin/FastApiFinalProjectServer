from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.dependencies import get_pet_service
from boundaries.requested_pet_boundary import RequestedPetBoundary
from errors.database_error import DatabaseError
from errors.not_found_error import NotFoundError
from errors.validation_error import ValidationError
from services.pet_service import PetService
from boundaries.pet_boundary import PetBoundary
from typing import List
import uuid

def get_pet_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=PetBoundary, summary="Create Pet")
    async def create_pet(
        pet_data: RequestedPetBoundary,
        db: AsyncSession = Depends(get_db),
        service: PetService = Depends(get_pet_service)
    ):
        try:
            pet = await service.create_pet(
                user_id=pet_data.user_id,  # Convert to UUID
                name=pet_data.name,
                species=pet_data.species,
                breed=pet_data.breed,
                date_of_birth=pet_data.date_of_birth,
                main_color=pet_data.main_color,
                pet_details=pet_data.pet_details,
                db=db
            )
            return pet
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.put("/{pet_id}", response_model=PetBoundary, summary="Update Pet")
    async def update_pet(
        pet_id: uuid.UUID,
        pet_data: RequestedPetBoundary,
        db: AsyncSession = Depends(get_db),
        service: PetService = Depends(get_pet_service)
    ):
        try:
            pet = await service.update_pet(
                pet_id=pet_id,  # Convert to UUID
                name=pet_data.name,
                species=pet_data.species,
                breed=pet_data.breed,
                date_of_birth=pet_data.date_of_birth,
                main_color=pet_data.main_color,
                pet_details=pet_data.pet_details,
                db=db
            )
            return pet
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{pet_id}", response_model=PetBoundary, summary="Get Pet by ID")
    async def get_pet_by_id(
            pet_id: uuid.UUID,
            db: AsyncSession = Depends(get_db),
            service: PetService = Depends(get_pet_service)
    ):
        try:
            pet = await service.get_pet_by_id(pet_id, db)  # Convert to UUID
            return pet
        except NotFoundError:
            raise HTTPException(status_code=404, detail="Pet not found.")
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/", response_model=List[PetBoundary], summary="Get All Pets with Pagination")
    async def get_all_pets(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        db: AsyncSession = Depends(get_db),
        service: PetService = Depends(get_pet_service)
    ):
        try:
            return await service.get_all_pets(page, size, db)
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/by-user/{user_id}", response_model=List[PetBoundary], summary="Get Pets by User ID with Pagination")
    async def get_pets_by_user_id(
        user_id: str,
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        db: AsyncSession = Depends(get_db),
        service: PetService = Depends(get_pet_service)
    ):
        try:
            return await service.get_pets_by_user_id(uuid.UUID(user_id), page, size, db)  # Convert to UUID
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
