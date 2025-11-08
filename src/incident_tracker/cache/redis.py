import json

from functools import lru_cache
from logging import getLogger
from typing import Any

from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import RedisError

from incident_tracker.interfaces.services import ICacheService
from incident_tracker.setup.config import settings

from .exceptions import RedisConnectionException, RedisOperationException

logger = getLogger(__name__)


class RedisCache(ICacheService):
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.instance: Redis | None = None

    def initialize(self) -> None:
        if not self.instance:
            try:
                pool = ConnectionPool().from_url(
                    self.redis_url,
                    decode_responses=True,
                )
                self.instance = Redis.from_pool(pool)
            except RedisError as e:
                logger.error("Ошибка инициализации Redis: %s", str(e))
                raise RedisConnectionException(
                    message="Ошибка инициализации Redis"
                ) from e

    async def set(self, key: str, value: Any, expire: int | None = None) -> None:
        try:
            if not isinstance(value, str):
                value = json.dumps(value)
            await self.instance.set(key, value, ex=expire)
        except Exception as e:
            logger.error("Ошибка записи: %s", str(e))
            raise RedisOperationException(message="Ошибка записи в редис") from e

    async def append(self, key: str, value: Any) -> None:
        data_set = await self.instance.get(key)
        try:
            data_set = json.loads(data_set) if data_set else []
            data_set.append(value)
            value = json.dumps(data_set)
            await self.instance.set(key, value)
        except Exception as e:
            logger.error("Ошибка добавления по ключу: %s", str(e))
            raise RedisOperationException(
                message="Ошибка добавления по ключу в редис"
            ) from e

    async def get(self, key: str) -> Any | None:
        try:
            value = await self.instance.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            logger.error("Ошибка чтения по ключу: %s", str(e))
            raise RedisOperationException(
                message="Ошибка чтения по ключу из редис"
            ) from e

    async def close_connection(self) -> None:
        await self.instance.connection_pool.disconnect()


@lru_cache
def get_redis() -> RedisCache:
    redis = RedisCache(settings.redis.url)
    redis.initialize()
    return redis
