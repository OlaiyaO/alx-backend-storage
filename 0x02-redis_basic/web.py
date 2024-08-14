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
    url = "http://slowwly.robertomurray.co.uk"

    @wraps(method)
    def wrapper(url):
        cached_key = "cached:" + url
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        store.incr(count_key)
        store.set(cached_key, html)
        store.expire(cached_key, 10)
        return html
    return wrapper


@count_url_access
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL."""
    res = requests.get(url)
    return res.text
