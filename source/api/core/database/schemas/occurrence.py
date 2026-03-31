import uuid

from pydantic import BaseModel, ConfigDict, field_validator

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape

from core.database.schemas.default import PaginatedResponse
from core.database.schemas.coordinates import CoordinateSchema
from core.database.models.incident import (
    IncidentType,
    IncidentIntensity,
    IncidentStatus,
)


class OccurrenceCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    location: CoordinateSchema

    type: IncidentType

    intensity: IncidentIntensity

    status: IncidentStatus


class OccurrenceReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    location: CoordinateSchema

    type: IncidentType

    intensity: IncidentIntensity

    status: IncidentStatus

    resolved_at: str | None = None

    resolved_by: uuid.UUID | None = None

    @field_validator("location", mode="before")
    @classmethod
    def convert_wkb_to_location(cls, value: any):

        if isinstance(value, WKBElement):
            point = to_shape(value)

            return {
                "longitude": point.x,
                "latitude": point.y,
            }

        return value


class OccurrenceUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    location: CoordinateSchema

    type: IncidentType

    intensity: IncidentIntensity

    status: IncidentStatus

    resolved_at: str | None = None

    resolved_by: uuid.UUID | None = None


class OccurrenceListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    occurrences: list[OccurrenceReadSchema]


class OccurrencePaginatedResponse(PaginatedResponse[OccurrenceReadSchema]):
    pass


class OccurrenceIndicatorsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_active: int

    affected_municipalities: int

    risk_level: str
