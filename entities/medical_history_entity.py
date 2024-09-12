from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base
import uuid


class MedicalHistoryEntity(Base):
    __tablename__ = "medical_histories"

    record_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.pet_id"), nullable=False)
    visit_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    diagnosis = Column(String, nullable=True)
    treatment = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    veterinarian_name = Column(String, nullable=True)

    # Relationships
    pet = relationship("PetEntity", back_populates="medical_histories")

    def __init__(self, pet_id: uuid.UUID, visit_date: datetime = None, diagnosis: str = None, treatment: str = None, notes: str = None, veterinarian_name: str = None):
        self.pet_id = pet_id
        self.visit_date = visit_date or datetime.utcnow()
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.notes = notes
        self.veterinarian_name = veterinarian_name

    def __eq__(self, other):
        return isinstance(other, MedicalHistoryEntity) and self.record_id == other.record_id

    def __str__(self):
        return f"MedicalHistoryEntity(record_id='{self.record_id}', pet_id='{self.pet_id}', visit_date='{self.visit_date}')"
