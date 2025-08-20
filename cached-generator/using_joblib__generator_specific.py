#!/usr/bin/env python
"""Add generator support to joblib.Memory forcibly.

The strategy is to shim a plain-old (cacheable) function between the inner,
original generator and the outer, cached generator.
"""

import typing
from functools import wraps
from typing import Callable
from typing import Generator

import joblib.memory
from joblib import Memory

memory = Memory(".cache", verbose=1)
T = typing.TypeVar("T")
P = typing.ParamSpec("P")


# TODO: I want a decorator that doesn't require it take a generator
def memory_cachei(ifunc: Callable[P, Generator[T]]):
    @wraps(ifunc)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> Generator[T]:
        generator: Generator[T]

        def stepped_func(
            *args: P.args, __iter__: int, **kwargs: P.kwargs
        ) -> None | tuple[T, int]:
            nonlocal generator

            if __iter__ < 0:
                generator = ifunc(*args, **kwargs)

            try:
                return next(generator), __iter__ + 1
            except StopIteration:
                return

        # help the joblib caching build good cache keys:
        stepped_func.__module__ = ifunc.__module__
        stepped_func.__name__ = ifunc.__name__
        stepped_func.__qualname__ = ifunc.__qualname__
        stepped_func: joblib.memory.MemorizedFunc = memory.cache(stepped_func)

        __iter__ = -1
        while result := stepped_func(*args, **kwargs, __iter__=__iter__):
            result, __iter__ = result
            yield result

    return wrapped


@memory_cachei
def h():
    for x in range(3):
        import time

        time.sleep(0.5)
        yield x


for x in h():
    print(x)
