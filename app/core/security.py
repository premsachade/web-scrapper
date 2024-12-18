import secrets

from fastapi import Security, status
from fastapi.security import APIKeyHeader

from app.core.config import settings
from app.exceptions import CustomHTTPException

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


async def verify_api_key(
    api_key: str = Security(api_key_header),
) -> None:
    if not api_key:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Missing API Key"
        )

    if not secrets.compare_digest(settings.API_KEY, api_key):
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Invalid API Key"
        )
