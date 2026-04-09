from enum import StrEnum


class IncidentType(StrEnum):
    FOREST_FIRE = "forest_fire"
    URBAN_FIRE = "urban_fire"


class IncidentIntensity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IncidentStatus(StrEnum):
    PENDING = "pending_confirmation"
    INVALIDATED = "invalidated"
    VALIDATED = "validated"
    RESOLVED = "resolved"
