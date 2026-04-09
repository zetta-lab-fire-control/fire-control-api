import uuid

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, field_validator, Field
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape


from core.database.schemas.default import PaginatedResponse
from core.database.schemas.coordinates import CoordinateSchema
from core.database.enums.incident import (
    IncidentType,
    IncidentIntensity,
    IncidentStatus,
)


class OccurrenceCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    location: CoordinateSchema = Field(
        ..., description="The location of the occurrence."
    )

    type: IncidentType = Field(..., description="The type of the occurrence.")

    intensity: IncidentIntensity = Field(
        ..., description="The intensity of the occurrence."
    )

    status: IncidentStatus = Field(..., description="The status of the occurrence.")


class OccurrenceReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="The ID of the occurrence.")

    location: CoordinateSchema = Field(
        ..., description="The location of the occurrence."
    )

    type: IncidentType = Field(..., description="The type of the occurrence.")

    intensity: IncidentIntensity = Field(
        ..., description="The intensity of the occurrence."
    )

    status: IncidentStatus = Field(..., description="The status of the occurrence.")

    city: str | None = Field(
        None, description="The city where the occurrence happened.", example="Lavras,MG"
    )

    resolved_at: datetime | None = Field(
        None, description="The date and time when the occurrence was resolved."
    )

    resolved_by: uuid.UUID | None = Field(
        None, description="The ID of the user who resolved the occurrence."
    )

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

    location: Optional[CoordinateSchema] = Field(
        None, description="The location of the occurrence."
    )

    city: Optional[str] = Field(
        None, description="The city where the occurrence happened.", example="Lavras,MG"
    )

    type: Optional[IncidentType] = Field(
        None, description="The type of the occurrence."
    )

    intensity: Optional[IncidentIntensity] = Field(
        None, description="The intensity of the occurrence."
    )

    status: Optional[IncidentStatus] = Field(
        None, description="The status of the occurrence."
    )

    resolved_at: Optional[datetime] = Field(
        None, description="The date and time when the occurrence was resolved."
    )

    resolved_by: Optional[uuid.UUID] = Field(
        None, description="The ID of the user who resolved the occurrence."
    )


class OccurrenceListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    occurrences: list[OccurrenceReadSchema] = Field(
        ..., description="The list of occurrences."
    )


class OccurrencePaginatedResponse(PaginatedResponse[OccurrenceReadSchema]):
    pass


class OccurrenceStatusCountSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    counts: Dict[IncidentStatus, int] = Field(
        ...,
        description="A dictionary containing the count of occurrences for each status.",
    )


class OccurrenceIntensityCountSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    counts: Dict[IncidentIntensity, int] = Field(
        ...,
        description="A dictionary containing the count of occurrences for each intensity.",
    )


class OccurrenceCityCountSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: str = Field(
        ..., description="The city where the occurrence happened.", example="Lavras,MG"
    )

    count: int = Field(..., description="The count of occurrences for the city.")


class OccurrenceHistorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    occurrences_count: int = Field(..., description="The total count of occurrences.")

    status_count: OccurrenceStatusCountSchema = Field(
        ..., description="The count of occurrences for each status."
    )

    intensity_count: OccurrenceIntensityCountSchema = Field(
        ..., description="The count of occurrences for each intensity."
    )

    cities_count: list[OccurrenceCityCountSchema] = Field(
        ..., description="The count of occurrences for each city."
    )

    start_date: datetime = Field(
        ..., description="The start date for the history period."
    )

    end_date: datetime = Field(..., description="The end date for the history period.")


class OccurrencePublicIndicatorsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    active_occurrences: int = Field(
        ..., description="The number of active occurrences."
    )

    affected_municipalities_count: int = Field(
        ..., description="The count of municipalities affected by occurrences."
    )

    risk_level: str = Field(
        ..., description="The risk level based on the current occurrences."
    )

    last_updated: datetime = Field(
        ..., description="The date and time when the indicators were last updated."
    )


class OccurrenceOperationalIndicatorsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status_count: OccurrenceStatusCountSchema = Field(
        ..., description="The count of occurrences for each status."
    )

    date: datetime = Field(
        ...,
        description="The date for which the indicators are calculated.",
        example="2024-06-01",
    )

    city: str = Field(
        ..., description="The city for which the indicators are calculated."
    )
