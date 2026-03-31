from sqlalchemy.orm import Session

from core.database.cruds import occurrence_crud


class OccurrenceService:
    def calculate__risk_score(self, total: int, avg_intensity: float) -> str:

        if total == 0:
            return "low"

        if avg_intensity >= 2.5 or total > 50:
            return "high"

        elif avg_intensity >= 1.5 or total > 20:
            return "medium"

        else:
            return "low"

    def get_indicators_data(self, db: Session) -> dict:

        raw_data = occurrence_crud.get_indicators_raw_data(db)

        if raw_data["total_active"] == 0:
            return {
                "total_active": 0,
                "affected_municipalities": 0,
                "risk_level": "low",
            }

        risk_level = self.calculate_risk_level(
            total=raw_data["total_active"], avg_intensity=raw_data["average_intensity"]
        )

        return {
            "total_active": raw_data["total_active"],
            "affected_municipalities": raw_data["affected_municipalities"],
            "risk_level": risk_level,
        }
