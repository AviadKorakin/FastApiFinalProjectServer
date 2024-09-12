from sqlalchemy import Column, String, Date, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import date
from entities.base import Base
import uuid

class PetEntity(Base):
    __tablename__ = "pets"

    pet_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)  # Keep UUID type for user_id
    name = Column(String, nullable=False)  # Add the name field here
    species = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    main_color = Column(String, nullable=True)
    pet_details = Column(JSON, nullable=True)

    # Relationships
    user = relationship("UserEntity", back_populates="pets")
    pet_images = relationship("PetImageEntity", back_populates="pet")
    medical_histories = relationship("MedicalHistoryEntity", back_populates="pet", cascade="all, delete-orphan")
    lost_pet_reports = relationship("LostPetReportEntity", back_populates="pet", cascade="all, delete-orphan", uselist=False)
    service_requests = relationship("ServiceRequestEntity", back_populates="pet", cascade="all, delete-orphan")

    def __init__(self, user_id: uuid.UUID, name: str, species: str, breed: str = None, date_of_birth: date = None,
                 main_color: str = None, pet_details: dict = None):
        # pet_id is auto-generated, no need to pass it as a parameter
        self.user_id = user_id
        self.name = name
        self.species = species
        self.breed = breed
        self.date_of_birth = date_of_birth
        self.main_color = main_color
        self.pet_details = pet_details or {}

    def __eq__(self, other):
        if isinstance(other, PetEntity):
            return self.pet_id == other.pet_id
        return False

    def __str__(self):
        return f"PetEntity(pet_id='{self.pet_id}', user_id='{self.user_id}', name='{self.name}', species='{self.species}', breed='{self.breed}', main_color='{self.main_color}', pet_details={self.pet_details})"
