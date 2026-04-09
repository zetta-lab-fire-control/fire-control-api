from core.database.cruds.default import CRUD
from core.database.models import Report
from core.database.schemas import ReportCreateSchema, ReportUpdateSchema


class ReportCRUD(CRUD[Report, ReportCreateSchema, ReportUpdateSchema]):
    def before_create(self, data: dict) -> dict:

        location = data.get("location")

        if location and isinstance(location, dict):
            lon = location.get("longitude", 0.0)

            lat = location.get("latitude", 0.0)

            data["location"] = f"SRID=4326;POINT({lon} {lat})"

        return data


report_crud = ReportCRUD(Report)
