from datetime import datetime

from sqlalchemy import func, case
from sqlalchemy.orm import Session
from geoalchemy2.types import Geography

from core.database.cruds.default import CRUD
from core.database.schemas import OccurrenceCreateSchema, OccurrenceUpdateSchema
from core.database.schemas.coordinates import CoordinateSchema
from core.database.models import Occurrence
from core.database.enums.incident import IncidentStatus, IncidentIntensity


class OccurrenceCRUD(CRUD[Occurrence, OccurrenceCreateSchema, OccurrenceUpdateSchema]):
    def __init__(self, model):

        super().__init__(model)

    def before_create(self, data) -> dict:

        location = data.get("location")

        if location and isinstance(location, dict):
            lon = location.get("longitude", 0.0)

            lat = location.get("latitude", 0.0)

            data["location"] = f"SRID=4326;POINT({lon} {lat})"

        return data

    def return_occurrence_within_radius(
        self, db: Session, point: CoordinateSchema, radius: float = 400
    ) -> Occurrence | None:

        # implementar lógica de escolha da ocorrência mais adequada, por enquanto retorna todas as ocorrências dentro do raio

        target_point = func.ST_SetSRID(
            func.ST_MakePoint(point.longitude, point.latitude), 4326
        )

        query = db.query(self.model).filter(
            func.ST_DWithin(
                func.cast(self.model.location, Geography),
                func.cast(target_point, Geography),
                radius,
            ),
            self.model.status == IncidentStatus.PENDING.value,
        )

        active_occurrence = query.first()

        return active_occurrence

    def return_public_indicators(self, db: Session):

        inactive_statuses = [
            IncidentStatus.RESOLVED.value,
            IncidentStatus.INVALIDATED.value,
        ]

        intensity_weight = case(
            (self.model.intensity == IncidentIntensity.LOW.value, 1),
            (self.model.intensity == IncidentIntensity.MEDIUM.value, 2),
            (self.model.intensity == IncidentIntensity.HIGH.value, 3),
            else_=0,
        )

        result = (
            db.query(
                func.count(self.model.id).label("active_occurrences"),
                func.count(func.distinct(self.model.city)).label(
                    "affected_municipalities_count"
                ),
                func.avg(intensity_weight).label("average_intensity"),
            )
            .filter(self.model.status.notin_(inactive_statuses))
            .first()
        )

        return {
            "active_occurrences": result.active_occurrences or 0,
            "affected_municipalities_count": result.affected_municipalities_count or 0,
            "average_intensity": float(result.average_intensity)
            if result.average_intensity
            else 0.0,
        }

    def return_operational_indicators(
        self, db: Session, city: str, target_date: datetime
    ) -> dict:
        """Busca contagem de status para uma cidade e data específicas."""

        query = (
            db.query(self.model.status, func.count(self.model.id).label("count"))
            .filter(
                self.model.city == city,
                func.date(self.model.created_at) == target_date.date(),
            )
            .group_by(self.model.status)
            .all()
        )

        status_counts = {status.value: 0 for status in IncidentStatus}

        for row in query:
            status_counts[row.status] = row.count

        return status_counts

    def return_history_indicators(
        self, db: Session, start_date: datetime, end_date: datetime
    ) -> dict:
        """Agrega dados históricos em um intervalo de tempo."""

        base_filter = [
            self.model.created_at >= start_date,
            self.model.created_at <= end_date,
        ]

        total_count = db.query(self.model).filter(*base_filter).count()

        status_query = (
            db.query(self.model.status, func.count(self.model.id))
            .filter(*base_filter)
            .group_by(self.model.status)
            .all()
        )
        status_counts = {row[0]: row[1] for row in status_query}

        intensity_query = (
            db.query(self.model.intensity, func.count(self.model.id))
            .filter(*base_filter)
            .group_by(self.model.intensity)
            .all()
        )
        intensity_counts = {row[0]: row[1] for row in intensity_query}

        city_query = (
            db.query(self.model.city, func.count(self.model.id))
            .filter(*base_filter)
            .group_by(self.model.city)
            .all()
        )
        city_counts = [
            {"city": row[0] or "Desconhecida", "count": row[1]} for row in city_query
        ]

        return {
            "total": total_count,
            "status_counts": status_counts,
            "intensity_counts": intensity_counts,
            "city_counts": city_counts,
        }


occurrence_crud = OccurrenceCRUD(Occurrence)
