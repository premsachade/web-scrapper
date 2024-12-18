import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup, ResultSet, Tag
from fastapi import BackgroundTasks

from app.core.config import settings
from app.core.redis import redis_client
from app.models.product import Product
from app.notification.console import ConsoleNotification
from app.storage.file import FileStorage


class Scrapper:
    __url = "https://dentalstall.com/shop/page"

    __session = aiohttp.ClientSession()

    __storer = FileStorage(f"{settings.DATA_DIRECTORY}/products.json")

    __notifier = ConsoleNotification(settings.EMAIL_RECIPIENTS)

    __max_retries = 3

    __wait_time = 3

    def __get_product_id(self, product_element: Tag) -> str:
        return (
            product_element.find("div", class_="mf-product-details")
            .find("h2", class_="woo-loop-product__title")
            .find("a", href=True)
            .get("href")
        )

    def __get_product_title(self, product_element: Tag) -> str:
        return (
            product_element.find("div", class_="mf-product-details")
            .find("h2", class_="woo-loop-product__title")
            .text
        )

    def __get_product_price(self, product_element: Tag) -> float:
        return float(
            product_element.find("div", class_="mf-product-price-box")
            .find("span", class_="woocommerce-Price-amount amount")
            .find("bdi")
            .text[1:]
        )

    def __get_product_image_url(self, product_element: Tag) -> str:
        return (
            product_element.find("div", class_="mf-product-thumbnail")
            .find(
                "img",
                class_="attachment-woocommerce_thumbnail size-woocommerce_thumbnail",
            )
            .get("data-lazy-src")
        )

    def __get_product_image_path(self, product_image_url: str) -> str:
        return f"{settings.IMAGES_DIRECTORY}/{product_image_url.split('/')[-1]}"

    async def __download_image(self, image_url: str, image_path: str) -> None:
        async with self.__session.get(image_url) as response:
            with open(image_path, "wb") as f:
                while True:
                    chunk = await response.content.read(1024)

                    if not chunk:
                        break

                    f.write(chunk)

    async def __download_images(self, products: dict[str, Product]) -> None:
        tasks = []

        for product in products.values():
            tasks.append(
                self.__download_image(
                    image_url=product.image_url, image_path=product.image_path
                )
            )

        await asyncio.gather(*tasks)

    async def __parse_single_page(
        self,
        page_number: int,
        proxy_url: str,
    ) -> dict[str, Product]:
        products = {}

        for attempt in range(self.__max_retries):
            try:
                async with self.__session.get(
                    f"{self.__url}/{page_number}", proxy=proxy_url
                ) as response:
                    response.raise_for_status()

                    html = await response.text()

                    soup = BeautifulSoup(html, "html.parser")

                    product_elements: list[ResultSet] = soup.find_all(
                        "div", class_="product-inner clearfix"
                    )

                    product_element: Tag
                    for product_element in product_elements:
                        product_id = self.__get_product_id(product_element)

                        product_title = self.__get_product_title(product_element)

                        product_price = self.__get_product_price(product_element)

                        product_image_url = self.__get_product_image_url(
                            product_element
                        )

                        product_image_path = self.__get_product_image_path(
                            product_image_url
                        )

                        cached_price = await redis_client.get(product_id)

                        if cached_price is None or float(cached_price) != product_price:
                            await redis_client.set(product_id, product_price, ex=600)

                        products[product_id] = Product(
                            title=product_title,
                            price=product_price,
                            image_url=product_image_url,
                            image_path=product_image_path,
                        )

                break
            except (aiohttp.ClientError, ValueError) as error:
                print(f"Error parsing page {page_number}: {error}")

                if attempt < self.__max_retries - 1:
                    print(f"Retrying in {self.__wait_time} seconds")

                    time.sleep(self.__wait_time)

        return products

    async def parse(
        self, background_tasks: BackgroundTasks, pages: int, proxy_url: str
    ) -> int:
        total_product_count = 0

        tasks = [
            self.__parse_single_page(page_number=page_number, proxy_url=proxy_url)
            for page_number in range(1, pages + 1)
        ]

        results = await asyncio.gather(*tasks)

        for products in results:
            parsed_products = {}

            for product_id, product in products.items():
                parsed_products[product_id] = {
                    "title": product.title,
                    "price": product.price,
                    "image_path": product.image_path,
                }

            self.__storer.save(parsed_products)

            product_count = len(products)

            total_product_count += product_count

            self.__notifier.send_message(
                f"Scrapped {product_count} web pages sucessfully"
            )

            background_tasks.add_task(self.__download_images, products)

        return total_product_count


scrapper = Scrapper()
