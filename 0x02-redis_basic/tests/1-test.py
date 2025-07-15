#!/usr/bin/python3
from exercise import Cache


# Assuming Cache class is defined as above
cache = Cache()

TEST_CASES = {
    b"foo": None,                   # Test raw bytes
    123: int,                       # Test integer conversion
    "bar": lambda d: d.decode("utf-8") # Test string conversion
}

for value, fn in TEST_CASES.items():
    key = cache.store(value) # Store the value
    assert cache.get(key, fn=fn) == value # Retrieve and assert equality
