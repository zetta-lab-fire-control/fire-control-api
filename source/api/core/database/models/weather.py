from sqlalchemy import Column, ForeignKey, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from core.database.models.default import DefaultModel


class WeatherZone(DefaultModel):
    __tablename__ = "zones"

    name = Column(String, nullable=False)

    geometry = Column(Geometry(geometry_type="POLYGON", srid=4326), nullable=False)

    weather_conditions = relationship(
        "WeatherConditions", back_populates="zone", cascade="all, delete-orphan"
    )


class WeatherConditions(DefaultModel):
    __tablename__ = "weather_conditions"

    temperature_celsius = Column(Float, nullable=True)

    relative_humidity = Column(Float, nullable=True)

    wind_speed_kmh = Column(Float, nullable=True)

    precipitation_mm = Column(Float, nullable=True)

    fire_risk_index = Column(Float, nullable=True)

    timestamp = Column(DateTime, nullable=False, index=True)

    zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=False)

    zone = relationship("WeatherZone", back_populates="weather_conditions")
