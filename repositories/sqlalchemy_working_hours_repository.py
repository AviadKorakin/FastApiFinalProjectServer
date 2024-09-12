from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from entities.working_hours_entity import WorkingHoursEntity
from errors.not_found_error import NotFoundError
from repositories.working_hours_repository import WorkingHoursRepository
from typing import List, Optional
import uuid  # Import UUID

class SQLAlchemyWorkingHoursRepository(WorkingHoursRepository):

    async def add_working_hours_bulk(self, working_hours: List[WorkingHoursEntity], db: AsyncSession) -> List[WorkingHoursEntity]:
        db.add_all(working_hours)
        await db.flush()  # Commit handled in the service
        return working_hours

    async def add_working_hours(self, working_hours: WorkingHoursEntity, db: AsyncSession) -> WorkingHoursEntity:
        db.add(working_hours)
        await db.flush()
        await db.refresh(working_hours)
        return working_hours

    async def update_working_hours(self, working_hours: WorkingHoursEntity, db: AsyncSession) -> WorkingHoursEntity:
        await db.flush()
        await db.refresh(working_hours)
        return working_hours

    async def remove_working_hours(self, working_hours_id: uuid.UUID, db: AsyncSession) -> None:
        working_hours = await db.get(WorkingHoursEntity, working_hours_id)
        if working_hours:
            await db.delete(working_hours)
            await db.flush()
        else:
            raise NotFoundError(f"Working hours with ID {working_hours_id} not found.")

    async def get_by_id(self, working_hours_id: uuid.UUID, db: AsyncSession) -> Optional[WorkingHoursEntity]:
        result = await db.execute(select(WorkingHoursEntity).filter_by(working_hours_id=working_hours_id))
        return result.scalar_one_or_none()

    async def get_by_provider_id(self, provider_id: uuid.UUID, db: AsyncSession, skip: int = 0, limit: int = 10) -> List[WorkingHoursEntity]:
        result = await db.execute(
            select(WorkingHoursEntity)
            .filter_by(provider_id=provider_id)
            .order_by(WorkingHoursEntity.day_of_week)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
