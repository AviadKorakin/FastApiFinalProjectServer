from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from errors.database_error import DatabaseError
from errors.not_found_error import NotFoundError
from errors.validation_error import ValidationError
from repositories.medical_history_repository import MedicalHistoryRepository
from entities.medical_history_entity import MedicalHistoryEntity
from services.medical_history_service import MedicalHistoryService
from typing import List, Optional
from datetime import datetime
import uuid


class MedicalHistoryServiceImplementation(MedicalHistoryService):

    def __init__(self, repository: MedicalHistoryRepository):
        self.repository = repository

    async def create_medical_history(self, pet_id: uuid.UUID, visit_date: datetime, diagnosis: Optional[str], treatment: Optional[str], notes: Optional[str], veterinarian_name: Optional[str], db: AsyncSession) -> MedicalHistoryEntity:
        medical_history = MedicalHistoryEntity(
            pet_id=pet_id,
            visit_date=visit_date,
            diagnosis=diagnosis,
            treatment=treatment,
            notes=notes,
            veterinarian_name=veterinarian_name
        )
        try:
            medical_history = await self.repository.create(medical_history, db)
            await db.commit()
            return medical_history
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "foreign key constraint" in error_message:
                raise ValidationError(f"Pet with ID '{pet_id}' does not exist.")
            raise DatabaseError(f"Medical history creation failed due to a database constraint: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred during medical history creation: {str(e)}")

    async def update_medical_history(self, record_id: uuid.UUID, pet_id: uuid.UUID, visit_date: datetime, diagnosis: Optional[str], treatment: Optional[str], notes: Optional[str], veterinarian_name: Optional[str], db: AsyncSession) -> MedicalHistoryEntity:
        medical_history = await self.repository.get_by_id(record_id, db)
        if not medical_history:
            raise NotFoundError(f"Medical history with ID '{record_id}' not found.")

        # Track if any data was actually updated
        has_updates = False

        # Check and apply updates if there are new values
        if pet_id and pet_id != medical_history.pet_id:
            medical_history.pet_id = pet_id
            has_updates = True
        if visit_date and visit_date != medical_history.visit_date:
            medical_history.visit_date = visit_date
            has_updates = True
        if diagnosis and diagnosis != medical_history.diagnosis:
            medical_history.diagnosis = diagnosis
            has_updates = True
        if treatment and treatment != medical_history.treatment:
            medical_history.treatment = treatment
            has_updates = True
        if notes and notes != medical_history.notes:
            medical_history.notes = notes
            has_updates = True
        if veterinarian_name and veterinarian_name != medical_history.veterinarian_name:
            medical_history.veterinarian_name = veterinarian_name
            has_updates = True

        # If there are no changes, skip the update
        if not has_updates:
            return medical_history  # Return the current state without updating the database

        try:
            medical_history = await self.repository.update(medical_history, db)
            await db.commit()
            return medical_history
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            raise ValidationError(f"Medical history update failed due to a database constraint: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred during medical history update: {str(e)}")

    async def create_all_medical_histories(self, medical_histories: List[MedicalHistoryEntity], db: AsyncSession) -> List[MedicalHistoryEntity]:
        try:
            medical_histories = await self.repository.create_all(medical_histories, db)
            await db.commit()
            return medical_histories
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            raise ValidationError(f"Bulk creation of medical histories failed due to a database constraint: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error occurred during bulk medical history creation: {str(e)}")

    async def get_medical_history_by_id(self, record_id: uuid.UUID, db: AsyncSession) -> Optional[MedicalHistoryEntity]:
        try:
            medical_history = await self.repository.get_by_id(record_id, db)
            if not medical_history:
                raise NotFoundError(f"Medical history with ID '{record_id}' not found.")
            return medical_history
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error retrieving medical history with ID '{record_id}': {str(e)}")

    async def filter_medical_histories(self, start_date: Optional[datetime], end_date: Optional[datetime], diagnosis: Optional[str], veterinarian_name: Optional[str], pet_id: Optional[uuid.UUID], db: AsyncSession) -> List[MedicalHistoryEntity]:
        try:
            return await self.repository.filter_by_criteria(start_date, end_date, diagnosis, veterinarian_name, pet_id, db)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error filtering medical histories: {str(e)}")
