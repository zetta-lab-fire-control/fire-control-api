from sqlalchemy import func, case
from sqlalchemy.orm import Session
from geoalchemy2.types import Geography

from core.database.cruds.default import CRUD
from core.database.schemas import OccurrenceCreateSchema, OccurrenceUpdateSchema
from core.database.schemas.coordinates import CoordinateSchema
from core.database.models import Occurrence
from core.database.models.incident import IncidentStatus, IncidentIntensity


class OccurrenceCRUD(CRUD[Occurrence, OccurrenceCreateSchema, OccurrenceUpdateSchema]):
    def __init__(self, model):
        super().__init__(model)

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

    def return_raw_indicators_data(self, db: Session):

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
                func.count(self.model.id).label("total_active"),
                func.count(func.distinct(self.model.city)).label(
                    "affected_municipalities"
                ),
                func.avg(intensity_weight).label("average_intensity"),
            )
            .filter(self.model.status.notin_(inactive_statuses))
            .first()
        )

        return {
            "total_active": result.total_active or 0,
            "affected_municipalities": result.affected_municipalities or 0,
            "average_intensity": float(result.average_intensity)
            if result.average_intensity
            else 0.0,
        }


occurrence_crud = OccurrenceCRUD(Occurrence)
