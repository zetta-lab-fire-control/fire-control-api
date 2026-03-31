from enum import StrEnum


class IncidentType(StrEnum):
    FIRE = "fire"


class IncidentIntensity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IncidentStatus(StrEnum):
    PENDING = "pending_confirmation"
    INVALIDATED = "invalidated"
    VALIDATED = "validated"
    RESOLVED = "resolved"
