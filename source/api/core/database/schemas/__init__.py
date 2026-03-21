from core.database.schemas.user import (
    UserCreateSchema,
    UserReadSchema,
    UserUpdateSchema,
    UserListSchema,
    UserLoginSchema,
    UserPaginatedResponse,
)
from core.database.schemas.report import (
    ReportRequestSchema,
    ReportCreateSchema,
    ReportReadSchema,
    ReportUpdateSchema,
    ReportListSchema,
    ReportPaginatedResponse,
)
from core.database.schemas.occurrence import (
    OccurrenceCreateSchema,
    OccurrenceReadSchema,
    OccurrenceUpdateSchema,
    OccurrenceListSchema,
    OccurrencePaginatedResponse,
)

from core.database.schemas.report_media import (
    ReportMediaCreateSchema,
    ReportMediaReadSchema,
    ReportMediaUpdateSchema,
    ReportMediaListSchema,
    ReportMediaPaginatedResponse,
)

from core.database.schemas.media import (
    MediaDownloadRequestSchema,
    MediaUploadRequestSchema,
    MediaResponseSchema,
)


__all__ = [
    "UserCreateSchema",
    "UserReadSchema",
    "UserUpdateSchema",
    "UserListSchema",
    "UserLoginSchema",
    "UserPaginatedResponse",
    "ReportRequestSchema",
    "ReportCreateSchema",
    "ReportReadSchema",
    "ReportUpdateSchema",
    "ReportListSchema",
    "ReportPaginatedResponse",
    "OccurrenceCreateSchema",
    "OccurrenceReadSchema",
    "OccurrenceUpdateSchema",
    "OccurrencePaginatedResponse",
    "OccurrenceListSchema",
    "MediaDownloadRequestSchema",
    "MediaUploadRequestSchema",
    "MediaResponseSchema",
    "ReportMediaCreateSchema",
    "ReportMediaReadSchema",
    "ReportMediaUpdateSchema",
    "ReportMediaListSchema",
    "ReportMediaPaginatedResponse",
]
