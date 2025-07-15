#!/usr/bin/env python3
"""
Web Cache & tracker module using Redis
"""
import requests
import redis
import functools
from typing import Callable

redis_client = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL,
    tracks access count, and caches the
    result with a 10-second expiration.
    """
    count_key = f"count:{url}"
    cache_key = f"cache:{url}"

    redis_client.incr(count_key)
    print(f"Incremented count for {url}. Current count: \
            {redis_client.get(count_key).decode('utf-8')}")

    cached_html = redis_client.get(cache_key)
    if cached_html:
        print(f"Cache hit for {url}")
        return cached_html.decode('utf-8')

    print(f"Cache miss for {url}. Fetching content...")
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text

    redis_client.setex(cache_key, 10, html_content)
    print(f"Cached {url} with expiration of 10 seconds.")

    return html_content

# Uncomment the below to test the web.py script


"""
if __name__ == "__main__":
    test_url_slow = "http://slowwly.robertomurray.co.uk/delay/5000/\
            url/http://www.google.com"
    test_url_fast = "http://example.com"

    print("--- Testing slow URL (first fetch) ---")
    print(f"Content length: {len(get_page(test_url_slow))}") \
            # First fetch, slow
    print("--- Testing slow URL (cached fetch) ---")
    print(f"Content length: {len(get_page(test_url_slow))}") \
            # Second fetch, should be fast (cache hit)
    import time
    time.sleep(11) # Wait for cache to expire
    print("--- Testing slow URL (after expiration) ---")
    print(f"Content length: {len(get_page(test_url_slow))}") \
            # Third fetch, slow again (cache miss)

    print("\n--- Testing fast URL ---")
    print(f"Content length: {len(get_page(test_url_fast))}")
    print(f"Content length: {len(get_page(test_url_fast))}")
"""
