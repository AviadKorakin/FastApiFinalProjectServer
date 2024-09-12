from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
import uuid

from boundaries.working_hours_boundary import WorkingHoursBoundary
from entities.working_hours_entity import WorkingHoursEntity
from repositories.working_hours_repository import WorkingHoursRepository
from services.working_hours_service import WorkingHoursService
from boundaries.working_hours_create_boundary import WorkingHoursCreateBoundary
from boundaries.working_hours_update_boundary import WorkingHoursUpdateBoundary
from errors.validation_error import ValidationError
from errors.database_error import DatabaseError


class WorkingHoursServiceImplementation(WorkingHoursService):
    def __init__(self, repository: WorkingHoursRepository):
        self.repository = repository

    async def add_working_hours(self, provider_id: uuid.UUID, working_hours_boundary: WorkingHoursCreateBoundary, db: AsyncSession) -> WorkingHoursEntity:
        working_hours_entity = WorkingHoursEntity(
            provider_id=provider_id,
            day_of_week=working_hours_boundary.working_hours.day_of_week,
            start_time=working_hours_boundary.working_hours.start_time,
            end_time=working_hours_boundary.working_hours.end_time
        )
        try:
            saved_working_hours = await self.repository.add_working_hours(working_hours_entity, db)
            await db.commit()
            return saved_working_hours
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "uq_provider_day" in error_message:
                raise ValidationError(f"Provider already has working hours for this day: {working_hours_boundary.working_hours.day_of_week}.")
            raise ValidationError(f"Failed to create working hours due to a database constraint: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error while creating working hours: {str(e)}")

    async def add_working_hours_bulk(self, provider_id: uuid.UUID, working_hours_list: List[WorkingHoursBoundary], db: AsyncSession) -> List[WorkingHoursEntity]:
        working_hours_entities = [
            WorkingHoursEntity(
                provider_id=provider_id,
                day_of_week=working_hour.day_of_week,
                start_time=working_hour.start_time,
                end_time=working_hour.end_time
            ) for working_hour in working_hours_list
        ]

        try:
            saved_working_hours = await self.repository.add_working_hours_bulk(working_hours_entities, db)
            await db.commit()
            return saved_working_hours
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            if "uq_provider_day" in error_message:
                raise ValidationError("Duplicate working hours for one or more days.")
            raise ValidationError(f"Failed to create working hours in bulk due to a database constraint: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error while adding working hours in bulk: {str(e)}")

    async def update_working_hours(self, working_hours_update: WorkingHoursUpdateBoundary, db: AsyncSession) -> WorkingHoursEntity:
        try:
            existing_working_hours = await self.repository.get_by_id(working_hours_update.working_hours_id, db)
            if not existing_working_hours:
                raise ValidationError(f"Working hours with ID {working_hours_update.working_hours_id} not found.")

            existing_working_hours.day_of_week = working_hours_update.day_of_week
            existing_working_hours.start_time = working_hours_update.start_time
            existing_working_hours.end_time = working_hours_update.end_time

            updated_working_hours = await self.repository.update_working_hours(existing_working_hours, db)
            await db.commit()
            return updated_working_hours
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            raise ValidationError(f"Failed to update working hours due to a database constraint: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error while updating working hours: {str(e)}")

    async def remove_working_hours(self, working_hours_id: uuid.UUID, db: AsyncSession) -> None:
        try:
            await self.repository.remove_working_hours(working_hours_id, db)
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            error_message = str(e.orig)
            raise ValidationError(f"Failed to remove working hours due to a database constraint: {error_message}")
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseError(f"Unexpected error while removing working hours: {str(e)}")

    async def get_by_provider_id(self, provider_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[WorkingHoursEntity]:
        try:
            return await self.repository.get_by_provider_id(provider_id, db, skip, limit)
        except SQLAlchemyError as e:
            raise DatabaseError(f"Error fetching working hours by provider ID '{provider_id}': {str(e)}")
