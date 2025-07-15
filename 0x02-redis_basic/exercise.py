#!/usr/bin/env python3
"""
Task 0: Writing strings to Redis (ln 84-95, 97-103).
Task 1: Reading from Redis and recovering
original type (ln 109-132).
Task 2: Incrementing values (ln 16-30).
Task 3: Storing lists (ln 33-56).
Task 4: Retrieving lists (ln 59-81)
"""
import redis
import uuid
import functools
from typing import Union, Callable, Any


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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs
    for a function. Appends inputs to
    '{method.__qualname__}:inputs' and outputs to
    '{method.__qualname__}:outputs' list in Redis.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        Wrapper function that stores inputs and outputs
        executes the original method.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, output)

        return output
    return wrapper


def replay(method: Callable):
    """
    Displays the history of calls of
    a particular function.
    """
    redis_instance = method.__self__._redis
    qualname = method.__qualname__

    call_count = redis_instance.get(qualname)
    if call_count:
        call_count = int(call_count.decode('utf-8'))
    else:
        call_count = 0

    inputs = redis_instance.lrange(f"{qualname}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{qualname}:outputs", 0, -1)

    print(f"{qualname} was called {call_count} times:")

    for input_args, output_val in zip(inputs, outputs):
        input_args_str = input_args.decode('utf-8')
        output_val_str = output_val.decode('utf-8')
        print(f"{qualname}(*{input_args_str}) -> {output_val_str}")


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

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis using a random key and
        returns the key. The data can be string, bytes, integer,
        or float. This method's calls are counted and
        inputs/outputs are historically stored.
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
