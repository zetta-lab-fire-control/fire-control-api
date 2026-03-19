from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes import router

from clients.postgres import PostgresClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    PostgresClient.connect()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Fire-Control-Api", version="0.0.0", lifespan=lifespan)

    app.include_router(router)

    return app


app = create_app()
