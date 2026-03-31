from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pathlib import Path
from redis import asyncio as aioredis

from routes import router

from clients.postgres import PostgresClient

description_path = Path(__file__).parent / "description.md"
version_path = Path(__file__).parent / "version.txt"


@asynccontextmanager
async def lifespan(app: FastAPI):

    PostgresClient.connect()

    redis = aioredis.from_url(
        "redis://localhost:6379", encoding="utf8", decode_responses=True
    )

    FastAPICache.init(RedisBackend(redis), prefix="api-cache")

    yield


def create_app() -> FastAPI:

    try:
        api_version = version_path.read_text(encoding="utf-8").strip()

    except FileNotFoundError:
        api_version = "0.0.0"

    try:
        api_description = description_path.read_text(encoding="utf-8").strip()

    except FileNotFoundError:
        api_description = ""

    app = FastAPI(
        title="Fire-Control-Api",
        version=api_version,
        description=api_description,
        lifespan=lifespan,
    )

    app.include_router(router)

    return app


app = create_app()
