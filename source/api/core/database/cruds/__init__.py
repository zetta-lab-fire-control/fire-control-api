from core.database.cruds.user import user_crud
from core.database.cruds.report import report_crud
from core.database.cruds.occurrence import occurrence_crud

__all__: list[str] = ["user_crud", "report_crud", "occurrence_crud"]
