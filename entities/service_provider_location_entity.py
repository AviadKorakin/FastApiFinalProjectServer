from geoalchemy2 import WKTElement
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography
from entities.base import Base
from utils.location import Location
import uuid


class ServiceProviderLocationEntity(Base):
    __tablename__ = "service_provider_locations"

    location_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("service_providers.provider_id"), nullable=False)
    full_address = Column(String, nullable=False)
    geo_location = Column(Geography(geometry_type='POINT', srid=4326), nullable=False)  # PostGIS location

    # Relationship to ServiceProviderEntity
    provider = relationship("ServiceProviderEntity", back_populates="locations")

    def __init__(self, provider_id: uuid.UUID, full_address: str, geo_location: Location):
        self.provider_id = provider_id
        self.full_address = full_address
        if geo_location:
            self.geo_location = WKTElement(f'POINT({geo_location.longitude} {geo_location.latitude})', srid=4326)

    def __eq__(self, other):
        return isinstance(other, ServiceProviderLocationEntity) and self.location_id == other.location_id

    def __str__(self):
        return f"ServiceProviderLocationEntity(location_id='{self.location_id}', provider_id='{self.provider_id}', full_address='{self.full_address}')"
