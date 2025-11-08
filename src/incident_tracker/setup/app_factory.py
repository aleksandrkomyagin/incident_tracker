from contextlib import asynccontextmanager
from logging import config, getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from incident_tracker.api import main_api_router
from incident_tracker.api.exception_handlers import register_exception_handler
from incident_tracker.api.middlewares.request_id_middleware import (
    RequestIDMiddleware,
)
from incident_tracker.cache.redis import get_redis
from incident_tracker.setup.config import APIConfig, settings
from incident_tracker.setup.di import dependency_container
from incident_tracker.setup.gunicorn import ApplicationServer, get_options
from incident_tracker.setup.logger import get_log_config

config.dictConfig(get_log_config())
logger = getLogger(__name__)


def start_redis(app: FastAPI):
    redis = get_redis()
    redis.initialize()
    app.state.redis = redis


def setup_dependencies(app: FastAPI):
    app.dependency_overrides.update(dependency_container)


def setup_routers(app: FastAPI):
    app.include_router(main_api_router)


def setup_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api_config.cors_origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIDMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_redis(app)
    yield
    app.state.redis.close_connection()


def init_app(debug: bool = False) -> FastAPI:
    app = FastAPI(
        debug=debug, title="Incident Tracker API", version="1.0.0", lifespan=lifespan
    )
    setup_dependencies(app)
    setup_routers(app)
    register_exception_handler(app)
    setup_middlewares(app)

    return app


def run_app(app: FastAPI, api_config: APIConfig) -> None:
    ApplicationServer(
        app,
        options=get_options(
            api_config.host,
            int(api_config.port),
            api_config.workers,
            get_log_config(),
        ),
    ).run()
