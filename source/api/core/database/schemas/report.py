from typing import Any
import uuid

from pydantic import BaseModel, ConfigDict, field_validator

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape

from core.database.schemas.default import PaginatedResponse
from core.database.schemas.coordinates import CoordinateSchema
from core.database.models.incident import IncidentType, IncidentIntensity
from core.database.schemas.report_media import ReportMediaListSchema


class ReportRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID

    location: CoordinateSchema

    type: IncidentType

    intensity: IncidentIntensity


class ReportCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID

    occurrence_id: uuid.UUID | None

    location: CoordinateSchema

    type: IncidentType

    intensity: IncidentIntensity


class ReportReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    user_id: uuid.UUID

    occurrence_id: uuid.UUID

    location: CoordinateSchema

    type: IncidentType

    intensity: IncidentIntensity

    media: ReportMediaListSchema = []

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


class ReportUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    user_id: uuid.UUID

    occurrence_id: uuid.UUID

    location: CoordinateSchema

    type: IncidentType

    intensity: IncidentIntensity

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
