import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from entities.medical_history_entity import MedicalHistoryEntity
from repositories.medical_history_repository import MedicalHistoryRepository
from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, nullslast


class SQLAlchemyMedicalHistoryRepository(MedicalHistoryRepository):
    async def create(self, medical_history: MedicalHistoryEntity, db: AsyncSession) -> MedicalHistoryEntity:
        db.add(medical_history)
        await db.flush()  # No commit here, handled by the service
        await db.refresh(medical_history)
        return medical_history

    async def update(self, medical_history: MedicalHistoryEntity, db: AsyncSession) -> MedicalHistoryEntity:
        await db.flush()  # No commit here, handled by the service
        await db.refresh(medical_history)
        return medical_history

    async def create_all(self, medical_histories: List[MedicalHistoryEntity], db: AsyncSession) -> List[MedicalHistoryEntity]:
        db.add_all(medical_histories)
        await db.flush()  # No commit here, handled by the service
        return medical_histories

    async def get_by_id(self, record_id: uuid.UUID, db: AsyncSession) -> Optional[MedicalHistoryEntity]:
        result = await db.execute(
            select(MedicalHistoryEntity).filter_by(record_id=record_id)
        )
        return result.scalar_one_or_none()

    async def filter_by_criteria(self, start_date: Optional[datetime], end_date: Optional[datetime],
                                 diagnosis: Optional[str], veterinarian_name: Optional[str],
                                 pet_id: Optional[uuid.UUID], db: AsyncSession) -> List[MedicalHistoryEntity]:
        query = select(MedicalHistoryEntity)

        # Date range filtering
        if start_date and end_date:
            query = query.where(MedicalHistoryEntity.visit_date.between(start_date, end_date))
        elif start_date:
            query = query.where(MedicalHistoryEntity.visit_date >= start_date)
        elif end_date:
            query = query.where(MedicalHistoryEntity.visit_date <= end_date)

        # Diagnosis filtering
        if diagnosis:
            query = query.where(MedicalHistoryEntity.diagnosis == diagnosis)

        # Veterinarian name filtering
        if veterinarian_name:
            query = query.where(MedicalHistoryEntity.veterinarian_name == veterinarian_name)

        # Pet ID filtering
        if pet_id:
            query = query.where(MedicalHistoryEntity.pet_id == pet_id)

        query = query.order_by(
            MedicalHistoryEntity.visit_date.desc(),
            nullslast(MedicalHistoryEntity.diagnosis.asc()),
            nullslast(MedicalHistoryEntity.veterinarian_name.asc())
        )

        result = await db.execute(query)
        return result.scalars().all()
