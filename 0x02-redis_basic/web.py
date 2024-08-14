#!/usr/bin/env python3
"""
Web cache and tracker module.
"""
import requests
import redis
from functools import wraps

store = redis.Redis()

def count_url_access(method):
    """Decorator to count how many times a URL is accessed."""
    @wraps(method)
    def wrapper(*args, **kwargs):
        # The URL is passed in the arguments
        url = args[0]
        cached_key = f"cached:{url}"
        cached_data = store.get(cached_key)

        # Return cached data if it exists
        if cached_data:
            return cached_data.decode("utf-8")

        # Get the HTML from the original function if not cached
        count_key = f"count:{url}"
        html = method(*args, **kwargs)

        # Increment the count for the URL and store the result in cache
        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)  # Cache expires in 10 seconds

        return html
    return wrapper

@count_url_access
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL."""
    res = requests.get(url)
    return res.text
