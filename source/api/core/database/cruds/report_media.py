from core.database.cruds.default import CRUD
from core.database.models import ReportMedia
from core.database.schemas import ReportMediaCreateSchema, ReportMediaUpdateSchema


class ReportMediaCRUD(
    CRUD[ReportMedia, ReportMediaCreateSchema, ReportMediaUpdateSchema]
):
    pass


report_media_crud = ReportMediaCRUD(ReportMedia)
