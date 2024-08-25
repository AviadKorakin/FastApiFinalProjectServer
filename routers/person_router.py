from fastapi import APIRouter, HTTPException, Path, Query, Depends

from app.dependencies import get_person_service
from services.person_service import PersonService
from boundaries.person_boundary import PersonBoundary

def get_person_router() -> APIRouter:
    router = APIRouter()

    @router.post("/{age}/", response_model=PersonBoundary)
    async def create_new_person(
        person: PersonBoundary,
        age: int = Path(..., ge=0),
        service: PersonService = Depends(get_person_service),  # Inject service here
    ):
        try:
            return service.create_person(first_name=person.first_name, last_name=person.last_name, age=age)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/", response_model=list[PersonBoundary])
    async def read_persons(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1),
        service: PersonService = Depends(get_person_service),  # Inject service here
    ):
        try:
            return service.get_persons(page=page, size=size)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/{person_id}/", response_model=PersonBoundary)
    async def get_person_by_id(
        person_id: int = Path(...),
        service: PersonService = Depends(get_person_service),  # Inject service here
    ):
        person = service.get_person_by_id(person_id)
        if person is None:
            raise HTTPException(status_code=404, detail="Person not found")
        return person

    return router
