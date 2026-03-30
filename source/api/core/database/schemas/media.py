from pydantic import BaseModel, ConfigDict

from enum import StrEnum


class MediaExtension(StrEnum):
    PNG = "png"

    MP4 = "mp4"

    PDF = "pdf"

    CSV = "csv"


class MediaDownloadRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bucket_name: str = "reports"

    extension_name: MediaExtension


class MediaUploadRequestSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bucket_name: str

    object_name: str


class MediaResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    bucket_name: str

    object_name: str

    object_url: str
