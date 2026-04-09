from core.database.cruds.default import CRUD
from core.database.models import MediaReport
from core.database.schemas import MediaReportCreateSchema, MediaReportUpdateSchema


class MediaReportCRUD(
    CRUD[MediaReport, MediaReportCreateSchema, MediaReportUpdateSchema]
):
    pass


media_report_crud = MediaReportCRUD(MediaReport)
