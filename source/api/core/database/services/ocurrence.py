from datetime import datetime

from sqlalchemy.orm import Session

from core.database.cruds import occurrence_crud


class OccurrenceService:
    def calculate_risk_score(self, total: int, avg_intensity: float) -> str:

        if total == 0:
            return "low"

        if avg_intensity >= 2.5 or total > 50:
            return "high"

        elif avg_intensity >= 1.5 or total > 20:
            return "medium"

        else:
            return "low"

    def get_public_indicators(self, db: Session) -> dict:

        raw_data = occurrence_crud.return_public_indicators(db)

        if raw_data["active_occurrences"] == 0:
            return {
                "active_occurrences": 0,
                "affected_municipalities_count": 0,
                "risk_level": "low",
            }

        risk_level = self.calculate_risk_score(
            total=raw_data["active_occurrences"],
            avg_intensity=raw_data["average_intensity"],
        )

        return {
            "active_occurrences": raw_data["active_occurrences"],
            "affected_municipalities_count": raw_data["affected_municipalities_count"],
            "risk_level": risk_level,
            "last_updated": datetime.now(),
        }

    def get_operational_indicators(
        self, db: Session, city: str, target_date: datetime
    ) -> dict:

        status_data = occurrence_crud.return_operational_indicators(
            db, city, target_date
        )

        return {
            "status_count": {"counts": status_data},
            "date": target_date,
            "city": city,
        }

    def get_history_indicators(
        self, db: Session, start_date: datetime, end_date: datetime
    ) -> dict:

        data = occurrence_crud.return_history_indicators(db, start_date, end_date)

        return {
            "occurrences_count": data["total"],
            "status_count": {"counts": data["status_counts"]},
            "intensity_count": {"counts": data["intensity_counts"]},
            "cities_count": data["city_counts"],
            "start_date": start_date,
            "end_date": end_date,
        }
