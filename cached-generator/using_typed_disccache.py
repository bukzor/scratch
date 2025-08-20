#!/usr/bin/env python
import logging

from typed_diskcache import Cache

logging.basicConfig(level=logging.DEBUG)

cache = Cache("./cache-dir")


def f():
    for x in range(3):
        import time

        time.sleep(0.5)
        yield x


for x in f():
    print(x)
