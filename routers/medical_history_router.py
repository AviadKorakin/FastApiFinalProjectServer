import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.dependencies import get_medical_history_service
from entities.medical_history_entity import MedicalHistoryEntity
from services.medical_history_service import MedicalHistoryService
from boundaries.requested_medical_history_boundary import RequestedMedicalHistoryBoundary
from boundaries.medical_history_boundary import MedicalHistoryBoundary
from errors.database_error import DatabaseError
from errors.not_found_error import NotFoundError
from errors.validation_error import ValidationError


def get_medical_history_router() -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=MedicalHistoryBoundary, summary="Create Medical History")
    async def create_medical_history(
        request: RequestedMedicalHistoryBoundary,
        service: MedicalHistoryService = Depends(get_medical_history_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.create_medical_history(
                pet_id=request.pet_id,
                visit_date=request.visit_date,
                diagnosis=request.diagnosis,
                treatment=request.treatment,
                notes=request.notes,
                veterinarian_name=request.veterinarian_name,
                db=db
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    @router.put("/{record_id}", response_model=MedicalHistoryBoundary, summary="Update Medical History")
    async def update_medical_history(
        record_id: uuid.UUID,
        request: RequestedMedicalHistoryBoundary,
        service: MedicalHistoryService = Depends(get_medical_history_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.update_medical_history(
                record_id=record_id,
                pet_id=request.pet_id,
                visit_date=request.visit_date,
                diagnosis=request.diagnosis,
                treatment=request.treatment,
                notes=request.notes,
                veterinarian_name=request.veterinarian_name,
                db=db
            )
        except NotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/{record_id}", response_model=MedicalHistoryBoundary, summary="Get Medical History by ID")
    async def get_medical_history_by_id(
        record_id: uuid.UUID,
        service: MedicalHistoryService = Depends(get_medical_history_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            medical_history = await service.get_medical_history_by_id(record_id, db)
            if not medical_history:
                raise HTTPException(status_code=404, detail="Medical history not found")
            return medical_history
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    @router.get("/", response_model=List[MedicalHistoryBoundary], summary="Filter Medical Histories")
    async def filter_medical_histories(
        start_date: Optional[datetime] = Query(None),
        end_date: Optional[datetime] = Query(None),
        diagnosis: Optional[str] = Query(None),
        veterinarian_name: Optional[str] = Query(None),
        pet_id: Optional[uuid.UUID] = Query(None),
        service: MedicalHistoryService = Depends(get_medical_history_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            return await service.filter_medical_histories(start_date, end_date, diagnosis, veterinarian_name, pet_id, db)
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    @router.post("/bulk", response_model=List[MedicalHistoryBoundary], summary="Create Multiple Medical Histories")
    async def create_all_medical_histories(
        requests: List[RequestedMedicalHistoryBoundary],
        service: MedicalHistoryService = Depends(get_medical_history_service),
        db: AsyncSession = Depends(get_db)
    ):
        try:
            medical_histories = [
                MedicalHistoryEntity(
                    pet_id=request.pet_id,
                    visit_date=request.visit_date,
                    diagnosis=request.diagnosis,
                    treatment=request.treatment,
                    notes=request.notes,
                    veterinarian_name=request.veterinarian_name
                ) for request in requests
            ]
            return await service.create_all_medical_histories(medical_histories, db)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except DatabaseError as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
