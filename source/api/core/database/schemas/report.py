from typing import Any
import uuid

from pydantic import BaseModel, ConfigDict, field_validator

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape

from core.database.schemas.default import PaginatedResponse
from core.database.schemas.coordinates import CoordinateSchema
from core.database.models.incident import IncidentType, IncidentIntensity


class ReportCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    occurrence_id: uuid.UUID
    location: CoordinateSchema
    type: IncidentType
    intensity: IncidentIntensity
    photo_url: str | None = None
    video_url: str | None = None


class ReportReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    occurrence_id: uuid.UUID
    location: CoordinateSchema
    type: IncidentType
    intensity: IncidentIntensity
    photo_url: str
    video_url: str


class ReportUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    occurrence_id: uuid.UUID
    location: CoordinateSchema
    type: IncidentType
    intensity: IncidentIntensity
    photo_url: str | None = None
    video_url: str | None = None

    @field_validator("location", mode="before")
    @classmethod
    def convert_wkb_to_location(cls, value: Any):

        if isinstance(value, WKBElement):
            point = to_shape(value)

            return {
                "longitude": point.x,
                "latitude": point.y,
            }

        return value


class ReportListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reports: list[ReportReadSchema]


class ReportPaginatedResponse(PaginatedResponse[ReportReadSchema]):
    pass
