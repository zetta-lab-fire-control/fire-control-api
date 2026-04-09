import uuid

from pydantic import BaseModel, ConfigDict, field_validator, Field
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from typing import Any, Optional

from core.database.schemas.default import PaginatedResponse
from core.database.schemas.coordinates import CoordinateSchema
from core.database.enums.incident import IncidentType, IncidentIntensity
from core.database.schemas.media_report import MediaReportReadSchema


class ReportRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID = Field(
        ..., description="The ID of the user who created the report."
    )

    location: CoordinateSchema = Field(..., description="The location of the report.")

    type: IncidentType = Field(..., description="The type of the incident.")

    intensity: IncidentIntensity = Field(
        ..., description="The intensity of the incident."
    )


class ReportCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID = Field(
        ..., description="The ID of the user who created the report."
    )

    occurrence_id: uuid.UUID = Field(
        ..., description="The ID of the occurrence associated with the report."
    )

    location: CoordinateSchema = Field(..., description="The location of the report.")

    type: IncidentType = Field(..., description="The type of the incident.")

    intensity: IncidentIntensity = Field(
        ..., description="The intensity of the incident."
    )


class ReportReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="The ID of the report.")

    user_id: uuid.UUID = Field(
        ..., description="The ID of the user who created the report."
    )

    occurrence_id: uuid.UUID = Field(
        ..., description="The ID of the occurrence associated with the report."
    )

    location: CoordinateSchema = Field(..., description="The location of the report.")

    type: IncidentType = Field(..., description="The type of the incident.")

    intensity: IncidentIntensity = Field(
        ..., description="The intensity of the incident."
    )

    media: list[MediaReportReadSchema] = Field(
        ..., description="The list of media associated with the report."
    )

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

    type: Optional[IncidentType] = Field(None, description="The type of the incident.")

    intensity: Optional[IncidentIntensity] = Field(
        None, description="The intensity of the incident."
    )


class ReportListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reports: list[ReportReadSchema] = Field(..., description="The list of reports.")


class ReportPaginatedResponse(PaginatedResponse[ReportReadSchema]):
    pass
