import json
from typing import Any
import redis
from app.core.config import settings


class Cache:
    def __init__(self) -> None:
        self.client = redis.from_url(settings.redis_url, decode_responses=True)

    def get_json(self, key: str) -> Any | None:
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except redis.RedisError:
            return None

    def set_json(self, key: str, value: Any, ttl_seconds: int) -> None:
        try:
            self.client.setex(key, ttl_seconds, json.dumps(value, default=str))
        except redis.RedisError:
            return

    def delete(self, key: str) -> None:
        try:
            self.client.delete(key)
        except redis.RedisError:
            return


cache = Cache()
