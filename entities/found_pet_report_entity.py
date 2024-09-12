from sqlalchemy import Column, DateTime, ForeignKey, String
from geoalchemy2 import Geography, WKTElement
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base
import uuid
from utils.location import Location


class FoundPetReportEntity(Base):
    __tablename__ = "found_pet_reports"

    report_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    report_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    geo_location = Column(Geography(geometry_type='POINT', srid=4326), nullable=True)
    description = Column(String, nullable=True)

    # Relationships
    found_pet_images = relationship("FoundPetImageEntity", back_populates="report")
    user = relationship("UserEntity", back_populates="found_pet_reports")

    def __init__(self, user_id: uuid.UUID, geo_location: Location = None, description: str = None):
        self.user_id = user_id
        self.report_date = datetime.utcnow()
        if geo_location:
            self.geo_location = WKTElement(f'POINT({geo_location.longitude} {geo_location.latitude})', srid=4326)
        self.description = description

    def __eq__(self, other):
        return isinstance(other, FoundPetReportEntity) and self.report_id == other.report_id

    def __str__(self):
        return f"FoundPetReportEntity(report_id='{self.report_id}', user_id='{self.user_id}', geo_location='{self.geo_location}')"
