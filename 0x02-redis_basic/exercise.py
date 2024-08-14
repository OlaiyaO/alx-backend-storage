#!/usr/bin/env python3
"""
Module declares a Redis Cache class and methods.
"""
import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increment the method call count."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Push input and output to Redis lists."""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return wrapper


def replay(fn: Callable):
    """Display the history of calls for a particular function."""
    r = redis.Redis()
    func_name = fn.__qualname__
    c = r.get(func_name)
    try:
        c = int(c.decode("utf-8"))
    except Exception:
        c = 0
    print(f"{func_name} was called {c} times:")
    inputs = r.lrange(f"{func_name}:inputs", 0, -1)
    outputs = r.lrange(f"{func_name}:outputs", 0, -1)
    for inp, outp in zip(inputs, outputs):
        inp = inp.decode("utf-8") if inp else ""
        outp = outp.decode("utf-8") if outp else ""
        print(f"{func_name}(*{inp}) -> {outp}")


class Cache:
    """Redis Cache class."""
    def __init__(self):
        """Initialize Redis connection and flush the database."""
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis and return a unique key."""
        rkey = str(uuid4())
        self._redis.set(rkey, data)
        return rkey

    def get(self, key: str, 
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Retrieve data from Redis, with optional type conversion."""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Retrieve a string value from Redis."""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Retrieve an integer value from Redis."""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
