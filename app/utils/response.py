from fastapi import status
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from pydantic_core import ErrorDetails


def create_response(
    status_code: int = status.HTTP_200_OK,
    success: bool = True,
    message: str = "",
    data: BaseModel | None = None,
    errors: list[ErrorDetails] | None = None,
) -> ORJSONResponse:
    content = {
        "success": success,
        "msg": message,
        "data": {},
    }

    if data:
        content["data"] = data.model_dump()

    if errors:
        content["errors"] = errors

    return ORJSONResponse(
        status_code=status_code,
        content=content,
    )
