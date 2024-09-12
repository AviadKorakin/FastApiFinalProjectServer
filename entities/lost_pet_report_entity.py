from sqlalchemy import Column, DateTime, ForeignKey, String
from geoalchemy2 import Geography, WKTElement
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base
import uuid
from utils.location import Location


class LostPetReportEntity(Base):
    __tablename__ = "lost_pet_reports"

    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    pet_id = Column(UUID(as_uuid=True), ForeignKey("pets.pet_id"), unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    report_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    geo_location = Column(Geography(geometry_type='POINT', srid=4326), nullable=True)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False)

    # Relationships
    user = relationship("UserEntity", back_populates="lost_pet_reports")
    pet = relationship("PetEntity", back_populates="lost_pet_reports")

    def __init__(self, pet_id: uuid.UUID, user_id: uuid.UUID, geo_location: Location = None, description: str = None, status: str = None):
        self.pet_id = pet_id
        self.user_id = user_id
        self.report_date = datetime.utcnow()
        if geo_location:
            self.geo_location = WKTElement(f'POINT({geo_location.longitude} {geo_location.latitude})', srid=4326)
        self.description = description
        self.status = status

    def __eq__(self, other):
        return isinstance(other, LostPetReportEntity) and self.report_id == other.report_id

    def __str__(self):
        return f"LostPetReportEntity(report_id='{self.report_id}', pet_id='{self.pet_id}', status='{self.status}')"
