import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


class LocationValidator:
    def __init__(self, engine: Engine | None = None):

        if engine:
            self.engine = engine
        else:
            database_url: str | None = os.getenv("DATABASE_URL")
            if not database_url:
                raise ValueError("DATABASE_URL não configurada.")
            self.engine = create_engine(database_url)

    def is_in_minas_gerais(self, latitude: float, longitude: float) -> bool:

        query = text("""
            SELECT 1
            FROM mg_cities
            WHERE ST_Contains(
                geometry,
                ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
            )
            LIMIT 1;
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"lon": longitude, "lat": latitude}).fetchone()

        return result is not None

    def get_city_name(self, latitude: float, longitude: float) -> str | None:

        query = text("""
            SELECT name
            FROM mg_cities
            WHERE ST_Contains(
                geometry,
                ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
            )
            LIMIT 1;
        """)

        with self.engine.connect() as conn:
            result = conn.execute(query, {"lon": longitude, "lat": latitude}).fetchone()

        return result[0] if result else None
