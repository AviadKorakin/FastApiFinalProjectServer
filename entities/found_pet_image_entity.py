from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from entities.base import Base
import uuid

class FoundPetImageEntity(Base):
    __tablename__ = "found_pet_images"

    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    report_id = Column(UUID(as_uuid=True), ForeignKey("found_pet_reports.report_id"), nullable=False)
    file_path = Column(String, nullable=False)  # Assuming this is the file path for S3 or similar storage
    url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to FoundPetReportEntity
    report = relationship("FoundPetReportEntity", back_populates="found_pet_images")

    def __init__(self, report_id: uuid.UUID, file_path: str, url: str, created_at: datetime = None):
        self.report_id = report_id
        self.file_path = file_path
        self.url = url
        self.created_at = created_at or datetime.utcnow()

    def __eq__(self, other):
        if isinstance(other, FoundPetImageEntity):
            return self.image_id == other.image_id
        return False

    def __str__(self):
        return f"FoundPetImageEntity(image_id='{self.image_id}', report_id='{self.report_id}', file_path='{self.file_path}', url='{self.url}', created_at='{self.created_at}')"
