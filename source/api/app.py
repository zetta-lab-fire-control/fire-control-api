from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Fire-Control-API", version="0.0.0", lifespan=lifespan)

    app.include_router(router)

    return app


app = create_app()
