import uuid

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from core.database.schemas.default import PaginatedResponse

from core.database.enums.media import Bucket, MediaExtension, MediaType


class MediaCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bucket: Bucket = Field(
        ..., description="The bucket where the media will be stored."
    )

    type: MediaType = Field(..., description="The type of the media.")

    extension: MediaExtension = Field(..., description="The extension of the media.")

    size: int = Field(..., description="The size of the media in bytes.")

    description: Optional[str] = Field(None, description="A description of the media.")


class MediaReadSchema(MediaCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="The ID of the media.")

    name: str = Field(..., description="The name of the media.")


class MediaUpdateSchema(MediaCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID = Field(..., description="The ID of the media.")

    name: str = Field(..., description="The name of the media.")


class MediaUploadResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    instance_metadata: MediaReadSchema = Field(
        ..., description="Metadata of the media instance that was created."
    )

    upload_url: str = Field(
        ..., description="The URL where the media can be uploaded to."
    )


class MediaDownloadResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    instance_metadata: MediaReadSchema = Field(
        ..., description="Metadata of the media instance that will be downloaded."
    )

    download_url: str = Field(
        ..., description="The URL from which the media can be downloaded."
    )


class MediaPaginatedResponse(PaginatedResponse[MediaReadSchema]):
    pass
