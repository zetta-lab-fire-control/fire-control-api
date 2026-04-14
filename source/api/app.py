from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis


from clients.postgres import PostgresClient
from docs import api_metadata
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    PostgresClient.connect()

    redis = aioredis.from_url(
        "redis://redis:6379", encoding="utf8", decode_responses=True
    )

    FastAPICache.init(RedisBackend(redis), prefix="api-cache")

    yield

    await redis.aclose()


def create_app() -> FastAPI:

    app = FastAPI(
        title="Fire-Control-Api",
        version=api_metadata["api_version"],
        description=api_metadata["api_description"],
        openapi_tags=api_metadata["api_tags"],
        lifespan=lifespan,
    )

    app.include_router(router)

    return app


app = create_app()
