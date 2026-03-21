import uuid

from pydantic import BaseModel, ConfigDict, computed_field

from core.database.schemas.default import PaginatedResponse
from core.storage.service import MinioService


class ReportMediaCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    report_id: uuid.UUID

    bucket_name: str

    object_name: str


class ReportMediaUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    report_id: uuid.UUID | None = None

    bucket_name: str | None = None

    object_name: str | None = None


class ReportMediaReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    report_id: uuid.UUID | None = None

    bucket_name: str | None = None

    object_name: str | None = None

    @computed_field
    @property
    def object_url(self) -> str | None:
        if self.bucket_name and self.object_name:
            try:
                storage = MinioService()
                return storage.generate_download_url(
                    bucket_name=self.bucket_name, object_name=self.object_name
                )
            except Exception:
                return None
        return None


class ReportMediaListSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    media: list[ReportMediaReadSchema]


class ReportMediaPaginatedResponse(PaginatedResponse[ReportMediaReadSchema]):
    pass
