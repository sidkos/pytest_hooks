from typing import Optional

import redis


class RedisClient:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self.connection: Optional[redis.Redis] = None

    def __enter__(self) -> "RedisClient":
        self.connection = redis.StrictRedis(host=self.host, port=self.port, db=self.db, decode_responses=True)
        if self.connection is None:
            raise RuntimeError("Failed to create a Redis connection.")
        self.connection.ping()  # Check if the Redis server is available
        print(f"Connected to Redis at {self.host}:{self.port}")
        return self

    def __exit__(
        self, exc_type: Optional[type], exc_value: Optional[BaseException], traceback: Optional[BaseException]
    ) -> None:
        if self.connection:
            print("Closing Redis connection.")
            self.connection.close()  # type: ignore[no-untyped-call]  # Suppress mypy error
        self.connection = None  # Reset the connection

    def post(self, key: str, value: str) -> bool:
        if not self.connection:
            raise RuntimeError("Redis connection is not established.")
        result = self.connection.set(key, value)
        return bool(result)

    def get(self, key: str) -> Optional[str]:
        if not self.connection:
            raise RuntimeError("Redis connection is not established.")
        result = self.connection.get(key)
        if result is None:
            return None
        if not isinstance(result, str):  # Ensure type safety
            raise TypeError(f"Expected str from Redis, got {type(result).__name__}.")
        return result
