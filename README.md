# Web Scrapper

## Features

- **Storage:**
  - Default: **File Storage** (`products.json`).
  - Easily extendable to other storage strategies by implementing the `Storage` abstract class.

- **Notification:**
  - Default: **Console Notification**.
  - Easily extendable to other notification strategies by implementing the `Notification` abstract class.

- **Caching:**
  - Uses `Redis` for storing updated product price.

## Prerequisites

- `Redis` must be running locally

## Setup

- Create an `.env` file in the root directory with the following variables

```properties
REDIS_URL = "redis://127.0.0.1:6379"

API_KEY = "rhAKV26VIsIQQo2Uoct6Gj3TRSLUWlt8HKyFiIuWHlc"

EMAIL_RECIPIENTS = ["test@test.com"]
```

- Install dependencies

```shell
pip3 install .
```

- Start server

```shell
uvicorn app.main:app --no-access-log --no-server-header --no-date-header --host 0.0.0.0 --port 8080
```

## Endpoints

- **GET** `/` - Health Check

- **GET** `/scrape` - Scrape Products

    | Query Parameters | Type | Description |
    |----------|----------|----------|
    | pages | integer | Number of pages to be scrapped |
    | proxy_url | string | Proxy URL to use while scrapping |

    | Headers | Type | Description |
    |----------|----------|----------|
    | x-api-key | string | Api Key for Authentication |

## TODO

- Use SQL Database([PostgreSQL](https://www.postgresql.org/)) for storing products.
- Use Blob Storage([MinIO](https://min.io/)) for storing images.
