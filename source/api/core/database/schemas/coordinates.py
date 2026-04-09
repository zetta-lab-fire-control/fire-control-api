from pydantic import BaseModel, Field


class CoordinateSchema(BaseModel):
    longitude: float = Field(
        ..., description="Longitude of the coordinate", example=12.345678
    )

    latitude: float = Field(
        ..., description="Latitude of the coordinate", example=-34.567890
    )
