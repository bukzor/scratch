#!/usr/bin/env python3
"""
Minimal generator caching - 20 lines of implementation code.
"""
from __future__ import annotations

import typing
from functools import wraps
from typing import Callable
from typing import Generator

import typed_diskcache as diskcache

# from typed_diskcache import Container

T = typing.TypeVar("T")
P = typing.ParamSpec("P")


class _Sentinel(str):
    def __repr__(self):
        return self


UNSET = _Sentinel("UNSET")
END = _Sentinel("END")

cache = diskcache.Cache(".cache")


def func_key(func: Callable[..., object]):
    code = func.__code__
    return (
        func.__module__,
        func.__qualname__,
        func.__defaults__,
        func.__kwdefaults__,
        code.co_code,
        code.co_consts,
        code.co_names,
        code.co_varnames,
        code.co_argcount,
        code.co_kwonlyargcount,
        code.co_posonlyargcount,
        code.co_freevars,
        code.co_cellvars,
    )


def memory_cache(func: Callable[P, Generator[T]]) -> Callable[P, Generator[T]]:
    """Cache generator results with persistence across processes."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Generator[T]:
        key = (func_key(func), args, tuple(sorted(kwargs.items())))

        try:
            yield from cache[key].value
        except KeyError:
            result: list[T] = []
            for item in func(*args, **kwargs):
                result.append(item)
                yield item
            cache[key] = result

    return wrapper


@memory_cache
def h(length=5):
    for x in range(length + 1):
        import time

        time.sleep(0.5)
        print(f"Computing {x}")
        yield x


def main():
    for x in h():
        print(f"Got {x}")


if __name__ == "__main__":
    raise SystemExit(main())
