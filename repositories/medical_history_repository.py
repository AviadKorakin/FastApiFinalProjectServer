from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from entities.medical_history_entity import MedicalHistoryEntity
from typing import List, Optional
from datetime import datetime
import uuid


class MedicalHistoryRepository(ABC):

    @abstractmethod
    async def create(self, medical_history: MedicalHistoryEntity, db: AsyncSession) -> MedicalHistoryEntity:
        pass

    @abstractmethod
    async def update(self, medical_history: MedicalHistoryEntity, db: AsyncSession) -> MedicalHistoryEntity:
        pass

    @abstractmethod
    async def create_all(self, medical_histories: List[MedicalHistoryEntity], db: AsyncSession) -> List[MedicalHistoryEntity]:
        pass

    @abstractmethod
    async def get_by_id(self, record_id: uuid.UUID, db: AsyncSession) -> Optional[MedicalHistoryEntity]:
        pass

    @abstractmethod
    async def filter_by_criteria(self, start_date: Optional[datetime], end_date: Optional[datetime],
                                 diagnosis: Optional[str], veterinarian_name: Optional[str],
                                 pet_id: Optional[uuid.UUID], db: AsyncSession) -> List[MedicalHistoryEntity]:
        pass
