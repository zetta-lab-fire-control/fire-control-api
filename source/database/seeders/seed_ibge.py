import json
import os
import requests
from sqlalchemy import create_engine, TextClause, text

from registry.mg_cities import mg_cities
from registry.north_mg_cities import north_mg_cities
from registry.test_mg_cities import LAVRAS_REGION_IBGE_CODES

DATABASE_URL = os.getenv("DATABASE_URL")
GEOJSON_URL = "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-31-mun.json"
IS_TEST_ENV = os.getenv("TEST", "false").lower() == "true"


def seed_mg_cities_data():

    print("Fetching MG cities data from IBGE...")

    response = requests.get(GEOJSON_URL, timeout=30.0)
    response.raise_for_status()
    geojson_data = response.json()

    print(f"Count: {len(geojson_data['features'])}")

    print("Seeding MG cities data into the database...")

    engine = create_engine(DATABASE_URL)

    count_inserted = 0

    target_cities = {
        city_code
        for city_code, city_name in mg_cities.items()
        if city_name in north_mg_cities.values()
    }

    not_encountered = {
        city_name
        for city_name in north_mg_cities.values()
        if city_name not in mg_cities.values()
    }

    print(f"Target cities count: {len(target_cities)}")
    print(
        f"Not encountered cities count: {len(not_encountered)}. IBGE codes: {not_encountered}"
    )

    with engine.begin() as conn:
        create_table: TextClause = text("""
            CREATE TABLE IF NOT EXISTS mg_cities (
                ibge_code VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                geometry GEOMETRY(MultiPolygon, 4326) NOT NULL
            );
        """)

        create_index: TextClause = text("""
            CREATE INDEX IF NOT EXISTS idx_mg_cities_geom ON mg_cities USING GIST (geometry);
        """)

        conn.execute(create_table)

        conn.execute(create_index)

        for feature in geojson_data["features"]:
            ibge_code = feature["properties"]["id"]

            name = feature["properties"]["name"]

            geometry_json = json.dumps(feature["geometry"])

            if IS_TEST_ENV and ibge_code not in LAVRAS_REGION_IBGE_CODES:
                continue

            if ibge_code not in target_cities:
                continue

            query = text("""
                INSERT INTO mg_cities (ibge_code, name, geometry)
                VALUES (:ibge_code, :name, ST_Multi(ST_SetSRID(ST_GeomFromGeoJSON(:geometry), 4326)))
                ON CONFLICT (ibge_code) DO NOTHING;
            """)

            conn.execute(
                query, {"ibge_code": ibge_code, "name": name, "geometry": geometry_json}
            )

            count_inserted += 1

    engine.dispose()

    print(f"MG cities data seeded successfully. Inserted: {count_inserted}")


if __name__ == "__main__":
    seed_mg_cities_data()
