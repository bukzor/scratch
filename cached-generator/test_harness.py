#!/usr/bin/env python
"""Add generator support to joblib.Memory forcibly.

The strategy is to shim a plain-old (cacheable) function between the inner,
original generator and the outer, cached generator.
"""

import typing
from functools import wraps
from typing import Callable
from typing import Generator

from joblib import Memory

memory = Memory(".cache", verbose=1)
T = typing.TypeVar("T")
P = typing.ParamSpec("P")


# TODO: I want a decorator that doesn't require it take a generator
def memory_cachei(ifunc: Callable[P, Generator[T]]):
    @wraps(ifunc)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> Generator[T]:
        # TODO fastpath if already computed, otherwise slowpath and cache
        yield from ifunc(*args, **kwargs)

    return wrapped


@memory_cachei
def h():
    for x in range(3):
        import time

        time.sleep(0.5)
        yield x


for x in h():
    print(x)
