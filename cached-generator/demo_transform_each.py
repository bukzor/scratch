import types
import typing
from functools import wraps
from typing import Callable

T = typing.TypeVar("T")
P = typing.ParamSpec("P")


def imap(transformer, generator):
    for x in generator:
        yield transformer(x)


def transformed(transformer: Callable[[T], T]):
    def decorator(f: Callable[P, T]):
        @wraps(f)
        def decorated(*args: P.args, **kwargs: P.kwargs) -> T:
            result = f(*args, **kwargs)
            if isinstance(result, types.GeneratorType):
                return imap(transformer, result)
            else:
                return transformer(result)
        return decorated
    return decorator



@transformed(lambda x: x+2)
def f0():
    return 10

@transformed(lambda x: x*x)
def f1():
    yield from range(4)

@transformed(lambda x: x*10)
def f2():
    for x in range(4):
        yield x

@transformed(lambda x: x*100)
def f3():
    for x in range(4):
        yield x


print(f0)
print(f0())

for f in (f1, f2, f3):
    print(f)
    print(tuple(f()))


__result__ = '''\
$ python demo_transform_each.py
<function f0 at 0x102d30720>
12
<function f1 at 0x102d30900>
(0, 1, 4, 9)
<function f2 at 0x102d30ae0>
(0, 10, 20, 30)
<function f3 at 0x102d30cc0>
(0, 100, 200, 300)
'''
