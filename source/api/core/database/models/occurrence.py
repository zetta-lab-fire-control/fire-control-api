from sqlalchemy import Column, ForeignKey, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from core.database.models.default import DefaultModel

from core.database.enums.incident import (
    IncidentType,
    IncidentIntensity,
    IncidentStatus,
    IncidentIgnitionCause,
    IncidentLandCover,
)


class Occurrence(DefaultModel):
    __tablename__ = "occurrences"

    type = Column(String, nullable=True, default=IncidentType.FOREST_FIRE.value)

    location = Column(Geometry(geometry_type="POINT", srid=4326), nullable=False)

    city = Column(String, nullable=True, index=True)

    intensity = Column(String, nullable=True, default=IncidentIntensity.LOW.value)

    status = Column(String, nullable=False, default=IncidentStatus.PENDING.value)

    resolved_at = Column(DateTime, nullable=True)

    resolved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    reports = relationship("Report", back_populates="occurrence")

    users = relationship("User", back_populates="occurrences")

    ignition_cause = Column(
        String, nullable=True, default=IncidentIgnitionCause.UNKNOWN.value
    )

    land_cover = Column(String, nullable=True, default=IncidentLandCover.UNKNOWN.value)

    burned_area = Column(Float, nullable=True, default=0.0)
