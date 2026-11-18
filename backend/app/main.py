from fastapi import FastAPI

from app.core.config import settings
from app.routers import health

app = FastAPI(
    title=settings.app_name,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(health.router)

