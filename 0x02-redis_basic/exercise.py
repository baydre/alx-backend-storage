#!/usr/bin/python3
"""
Task 0: Writing strings to Redis.
"""
import redis
import uuid
from typing import Union, Callable, Any


class Cache:
    """
    Cache class for interacting with Redis
    """
    def __init__(self):
        """
        Initializes a Cache instance with
        a Redis client and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis using
        a random key and returns the key.The data
        can be a string, bytes, integer, or float.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
