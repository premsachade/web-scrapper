from redis import asyncio as aioredis

from app.core.config import settings

redis_client = aioredis.Redis.from_url(settings.REDIS_URL)
