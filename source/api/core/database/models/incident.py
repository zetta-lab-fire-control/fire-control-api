from enum import StrEnum


class IncidentType(StrEnum):
    FIRE = "fire"


class IncidentIntensity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IncidentStatus(StrEnum):
    PENDING = "pending_confirmation"
    VALIDATED = "validated"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FALSE_ALERT = "false_alert"
