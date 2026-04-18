from core.database.schemas.user import (
    UserCreateSchema,
    UserReadSchema,
    UserUpdateSchema,
    UserListSchema,
    UserLoginSchema,
    UserPaginatedResponse,
    UserAuthSchema,
    AdminCreateSchema,
    FirefighterCreateSchema,
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
    OccurrenceHistorySchema,
    OccurrencePublicIndicatorsSchema,
    OccurrenceOperationalIndicatorsSchema,
)

from core.database.schemas.media import (
    MediaCreateSchema,
    MediaReadSchema,
    MediaUpdateSchema,
    MediaPaginatedResponse,
    MediaDownloadResponseSchema,
    MediaUploadResponseSchema,
)

from core.database.schemas.media_report import (
    MediaReportCreateSchema,
    MediaReportReadSchema,
    MediaReportUpdateSchema,
    MediaReportListSchema,
    MediaReportPaginatedResponse,
)

from core.database.schemas.default import PaginatedResponse

from core.database.schemas.auth import (
    TokenSchema,
    AcessTokenSchema,
    RefreshTokenSchema,
    ResetTokenSchema,
    PasswordRequestSchema,
    PasswordResetSchema,
)

__all__ = [
    "UserCreateSchema",
    "UserReadSchema",
    "UserUpdateSchema",
    "UserListSchema",
    "UserLoginSchema",
    "UserPaginatedResponse",
    "UserAuthSchema",
    "AdminCreateSchema",
    "FirefighterCreateSchema",
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
    "OccurrenceHistorySchema",
    "OccurrencePublicIndicatorsSchema",
    "OccurrenceOperationalIndicatorsSchema",
    "MediaDownloadResponseSchema",
    "MediaUploadResponseSchema",
    "MediaCreateSchema",
    "MediaReadSchema",
    "MediaUpdateSchema",
    "MediaPaginatedResponse",
    "MediaReportCreateSchema",
    "MediaReportReadSchema",
    "MediaReportUpdateSchema",
    "MediaReportListSchema",
    "MediaReportPaginatedResponse",
    "PaginatedResponse",
    "TokenSchema",
    "AcessTokenSchema",
    "RefreshTokenSchema",
    "PasswordRequestSchema",
    "PasswordResetSchema",
    "ResetTokenSchema",
]
