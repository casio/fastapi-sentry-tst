from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

import redis.asyncio as aioredis
from src import redis
from src.auth.router import router as auth_router
from src.config import app_configs, settings
from src.external_service.router import router as external_service_router

TMPL = Path(__file__).parent / "tmpl"


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    pool = aioredis.ConnectionPool.from_url(
        str(settings.REDIS_URL), max_connections=10, decode_responses=True
    )
    redis.redis_client = aioredis.Redis(connection_pool=pool)

    yield

    if settings.ENVIRONMENT.is_testing:
        return
    # Shutdown
    await pool.disconnect()


app = FastAPI(**app_configs, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENVIRONMENT,
    enable_tracing=True,
    # traces_sample_rate=1.0,
    # enable_profiling=True,
    profiles_sample_rate=1.0,
)


@app.get("/")
async def home() -> dict[str, str]:
    return FileResponse(TMPL / "index.html", media_type="text/html")


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(
    external_service_router, prefix="/external-service", tags=["External Service Calls"]
)


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
