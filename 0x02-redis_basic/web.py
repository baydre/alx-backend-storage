#!/usr/bin/env python3
"""
Web cache and tracker module using Redis, implemented with a decorator.
"""
import requests
import redis
import functools
from typing import Callable

redis_client = redis.Redis()


def cache_and_track_url(method: Callable) -> Callable:
    """
    Decorator that tracks URL access count and caches
    the result with expiration.
    """
    @functools.wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function that implements caching and tracking logic.
        """
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        redis_client.incr(count_key)

        cached_html = redis_client.get(cache_key)
        if cached_html:
            return cached_html.decode('utf-8')

        html_content = method(url)

        redis_client.setex(cache_key, 10, html_content)

        return html_content
    return wrapper


@cache_and_track_url
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL.
    This function is now wrapped by the cache_and_track_url decorator.
    """
    print(f"Fetching actual content for: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text
