import uuid

from pydantic import BaseModel, ConfigDict, Field

from core.database.schemas.default import PaginatedResponse


class MediaReportCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    media_id: uuid.UUID = Field(
        ...,
        description="ID of the media",
        example="123e4567-e89b-12d3-a456-426614174000",
    )

    report_id: uuid.UUID = Field(
        ...,
        description="ID of the report",
        example="123e4567-e89b-12d3-a456-426614174000",
    )


class MediaReportReadSchema(MediaReportCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(
        ...,
        description="ID of the media report",
        example="123e4567-e89b-12d3-a456-426614174000",
    )


class MediaReportUpdateSchema(MediaReportCreateSchema):
    pass


class MediaReportListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    media: list[MediaReportReadSchema]


class MediaReportPaginatedResponse(PaginatedResponse[MediaReportReadSchema]):
    pass
