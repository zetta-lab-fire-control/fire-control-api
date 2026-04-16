from enum import Enum
from pydantic import BaseModel, Field, model_validator

from core.database.services.location import LocationValidator


class MinasGeraisBoundingBox(Enum):
    MIN_LAT = -22.00
    MAX_LAT = -14.00
    MIN_LON = -51.00
    MAX_LON = -39.00


class CoordinateSchema(BaseModel):
    longitude: float = Field(
        ...,
        ge=MinasGeraisBoundingBox.MIN_LON.value,
        le=MinasGeraisBoundingBox.MAX_LON.value,
        description="Longitude. Restrita aos limites leste/oeste de MG.",
        json_schema_extra={"example": -44.9975},
    )

    latitude: float = Field(
        ...,
        ge=MinasGeraisBoundingBox.MIN_LAT.value,
        le=MinasGeraisBoundingBox.MAX_LAT.value,
        description="Latitude. Restrita aos limites norte/sul de MG.",
        json_schema_extra={"example": -21.2464},
    )

    @model_validator(mode="after")
    def validate_postgis(self) -> "CoordinateSchema":

        db_validator = LocationValidator()

        city = db_validator.get_city_name(self.latitude, self.longitude)

        if not city:
            raise ValueError(
                f"The provided coordinates (lat: {self.latitude}, lon: {self.longitude}) are outside the boundaries of Minas Gerais."
            )

        # TODO: ADD CITY_NAME
        # self.city_name = city

        return self
