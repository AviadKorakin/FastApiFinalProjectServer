from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from entities.medical_history_entity import MedicalHistoryEntity
from typing import List, Optional
from datetime import datetime
import uuid


class MedicalHistoryService(ABC):

    @abstractmethod
    async def create_medical_history(self, pet_id: uuid.UUID, visit_date: datetime, diagnosis: Optional[str],
                                     treatment: Optional[str], notes: Optional[str],
                                     veterinarian_name: Optional[str], db: AsyncSession) -> MedicalHistoryEntity:
        pass

    @abstractmethod
    async def update_medical_history(self, record_id: uuid.UUID, pet_id: uuid.UUID, visit_date: datetime,
                                     diagnosis: Optional[str], treatment: Optional[str],
                                     notes: Optional[str], veterinarian_name: Optional[str],
                                     db: AsyncSession) -> MedicalHistoryEntity:
        pass

    @abstractmethod
    async def create_all_medical_histories(self, medical_histories: List[MedicalHistoryEntity], db: AsyncSession) -> List[MedicalHistoryEntity]:
        pass

    @abstractmethod
    async def get_medical_history_by_id(self, record_id: uuid.UUID, db: AsyncSession) -> Optional[MedicalHistoryEntity]:
        pass

    @abstractmethod
    async def filter_medical_histories(self, start_date: Optional[datetime], end_date: Optional[datetime],
                                       diagnosis: Optional[str], veterinarian_name: Optional[str],
                                       pet_id: Optional[uuid.UUID], db: AsyncSession) -> List[MedicalHistoryEntity]:
        pass
