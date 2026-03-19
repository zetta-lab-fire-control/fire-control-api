from pydantic import BaseModel


class CoordinateSchema(BaseModel):
    longitude: float

    latitude: float
