from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import ORJSONResponse

from app.helpers.scraper import scrapper
from app.schemas.scrape import ScrapeResponseData
from app.utils.response import create_response

router = APIRouter(tags=["Scrape"])


@router.get("/scrape", status_code=status.HTTP_200_OK)
async def scrape(
    background_tasks: BackgroundTasks, pages: int = 1, proxy_url: str = ""
) -> ORJSONResponse:
    product_count = await scrapper.parse(
        background_tasks=background_tasks,
        pages=pages,
        proxy_url=proxy_url,
    )

    return create_response(
        status_code=status.HTTP_200_OK,
        message="Scraping Results",
        data=ScrapeResponseData(product_count=product_count),
    )
