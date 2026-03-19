from sqlalchemy import func
from sqlalchemy.orm import Session
from geoalchemy2.types import Geography

from core.database.cruds.default import CRUD
from core.database.schemas import OccurrenceCreateSchema, OccurrenceUpdateSchema
from core.database.schemas.coordinates import CoordinateSchema
from core.database.models import Occurrence
from core.database.models.incident import IncidentStatus


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


occurrence_crud = OccurrenceCRUD(Occurrence)
