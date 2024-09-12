from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from errors.database_error import DatabaseError
from errors.not_found_error import NotFoundError
from errors.validation_error import ValidationError
from repositories.pet_repository import PetRepository
from entities.pet_entity import PetEntity
from services.pet_service import PetService
from typing import List
from datetime import date
import uuid

class PetServiceImplementation(PetService):

    def __init__(self, repository: PetRepository):
        self.repository = repository

    async def create_pet(self, user_id: uuid.UUID, name: str, species: str, breed: str, date_of_birth: date, main_color: str, pet_details: dict, db: AsyncSession) -> PetEntity:
        pet = PetEntity(
            user_id=user_id,
            name=name,
            species=species,
            breed=breed,
            date_of_birth=date_of_birth,
            main_color=main_color,
            pet_details=pet_details
        )
        try:
            pet = await self.repository.create(pet, db)
            await db.commit()
            return pet
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "foreign key constraint" in error_message:
                raise ValidationError(f"User with ID '{user_id}' does not exist.")
            raise DatabaseError(f"Pet creation failed due to a database error: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred during pet creation: {str(e)}")

    async def update_pet(self, pet_id: uuid.UUID, name: str, species: str, breed: str, date_of_birth: date, main_color: str, pet_details: dict, db: AsyncSession) -> PetEntity:
        pet = await self.repository.get_by_pet_id(pet_id, db)
        if not pet:
            raise NotFoundError(f"Pet with ID '{pet_id}' not found.")

        pet.name = name
        pet.species = species
        pet.breed = breed
        pet.date_of_birth = date_of_birth
        pet.main_color = main_color
        pet.pet_details = pet_details

        try:
            pet = await self.repository.update(pet, db)
            await db.commit()
            return pet
        except IntegrityError as e:
            await db.rollback()
            raise DatabaseError(f"Pet update failed due to a database error: {str(e.orig)}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred during pet update: {str(e)}")

    async def get_pet_by_id(self, pet_id: uuid.UUID, db: AsyncSession) -> PetEntity | None:
        try:
            pet = await self.repository.get_by_pet_id(pet_id, db)
            if not pet:
                raise NotFoundError(f"Pet with ID '{pet_id}' not found.")
            return pet
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error fetching pet with ID '{pet_id}': {str(e)}")

    async def get_all_pets(self, page: int, size: int, db: AsyncSession) -> List[PetEntity]:
        skip = (page - 1) * size
        try:
            return await self.repository.get_all(skip=skip, limit=size, db=db)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error fetching all pets: {str(e)}")

    async def get_pets_by_user_id(self, user_id: uuid.UUID, page: int, size: int, db: AsyncSession) -> List[PetEntity]:
        skip = (page - 1) * size
        try:
            return await self.repository.get_by_user_id(user_id, skip=skip, limit=size, db=db)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error fetching pets for user with ID '{user_id}': {str(e)}")
