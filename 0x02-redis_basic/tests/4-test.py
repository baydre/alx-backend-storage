#!/usr/bin/env python3
from exercise import Cache, replay


# Assuming Cache class and replay function are defined as above
cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)

replay(cache.store)
