from typing import List, Optional

import redis


class RedisClient:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self.connection: Optional[redis.Redis] = None

    def __enter__(self) -> "RedisClient":
        self.connection = redis.StrictRedis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True,
        )
        if not self.connection:
            raise RuntimeError("Failed to create a Redis connection.")
        return self

    def __exit__(
        self, exc_type: Optional[type], exc_value: Optional[BaseException], traceback: Optional[BaseException]
    ) -> None:
        if self.connection:
            self.connection.close()  # type: ignore[no-untyped-call]
        self.connection = None

    def post(self, key: str, value: str) -> bool:
        if not self.connection:
            raise RuntimeError("Redis connection is not established.")
        return bool(self.connection.set(key, value))

    def get(self, key: str) -> Optional[str]:
        if not self.connection:
            raise RuntimeError("Redis connection is not established.")
        result = self.connection.get(key)
        return str(result) if result is not None else None

    def keys(self, pattern: str) -> List[str]:
        if not self.connection:
            raise RuntimeError("Redis connection is not established.")
        result = self.connection.keys(pattern)
        return list(result) if isinstance(result, list) else []

    def delete(self, key: str) -> bool:
        if not self.connection:
            raise RuntimeError("Redis connection is not established.")
        return bool(self.connection.delete(key))

    def exists(self, key: str) -> bool:
        if not self.connection:
            raise RuntimeError("Redis connection is not established.")
        return bool(self.connection.exists(key))

    def flushdb(self) -> None:
        if not self.connection:
            raise RuntimeError("Redis connection is not established.")
        self.connection.flushdb()
