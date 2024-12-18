from pydantic import BaseModel

from app.schemas.response import Response


class ScrapeResponseData(BaseModel):
    product_count: int


class ScrapeResponse(Response):
    data: ScrapeResponseData
