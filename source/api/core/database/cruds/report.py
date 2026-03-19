from core.database.cruds.default import CRUD
from core.database.models import Report
from core.database.schemas import ReportCreateSchema, ReportUpdateSchema


class ReportCRUD(CRUD[Report, ReportCreateSchema, ReportUpdateSchema]):
    pass


report_crud = ReportCRUD(Report)
