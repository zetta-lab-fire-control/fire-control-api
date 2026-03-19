from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from core.database.models.default import DefaultModel
from core.database.models.incident import IncidentType, IncidentIntensity


class Report(DefaultModel):
    __tablename__ = "reports"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    occurrence_id = Column(
        UUID(as_uuid=True), ForeignKey("occurrences.id"), nullable=True
    )

    type = Column(String, nullable=True, default=IncidentType.FIRE.value)

    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)

    intensity = Column(String, nullable=True, default=IncidentIntensity.LOW.value)

    photo_url = Column(String, nullable=True)

    video_url = Column(String, nullable=True)

    user = relationship("User", back_populates="reports")

    occurrence = relationship("Occurrence", back_populates="reports")
