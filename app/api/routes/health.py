from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from app.utils.response import create_response

router = APIRouter(tags=["Health Checkup"])


@router.get("/")
async def root() -> ORJSONResponse:
    return create_response(message="app running")
