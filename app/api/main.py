from fastapi import APIRouter, Depends

from app.api.routes import health, scrape
from app.core.security import verify_api_key

api_router = APIRouter()


api_router.include_router(health.router)
api_router.include_router(
    scrape.router,
    dependencies=[Depends(verify_api_key)],
)
