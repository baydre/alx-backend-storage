#!/usr/bin/env python3
"""
Task 0: Writing strings to Redis (ln 1-32).
Task 1: Reading from Redis and recovering
original type (ln 36-59).
Task 2: Incrementing values (ln 61-86).
"""
import redis
import uuid
import functools
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

    def get(self, key: str, fn: Callable = None) -> \
            Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis and optionally converts it
        using a callable If the key does not exist, returns None.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve data from Redis as a UTF-8 string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves data from Redis as an integer.
        """
        return self.get(key, fn=int)

    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count how many times a method is called.
        Uses the method's qualified name as a Redis key for
        the counter.
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs) -> Any:
            """
            Wrapper function that increments the call count
            and executes the original method.
            """
            self._redis.incr(method.__qualname__)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and
        returns the key. The data can be a string, bytes, integer,
        or float. This methods's calls are counted.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
