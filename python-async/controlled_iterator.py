from __future__ import annotations

import asyncio
from asyncio import Future
from typing import Any
from typing import TypeVar

T = TypeVar("T")


class ControlledIterator[T]:
    future: Future[T]

    def __init__(self):
        super().__init__()
        self.future = Future()

    def __aiter__(self):
        return self

    async def __anext__(self) -> T:
        try:
            return await self.future
        except asyncio.CancelledError:
            raise StopAsyncIteration
        finally:
            self.future = Future()


async def test_controlled_iterator():
    c = ControlledIterator[int]()
    xs = aiter(c)

    # Use anext() to get the next value without blocking indefinitely
    coro = anext(xs)

    future = asyncio.ensure_future(coro)

    # The future shouldn't be done yet since we haven't sent a value
    assert not future.done()

    # Send a value using the future interface directly
    c.future.set_result(42)

    # Check that we receive the value
    x = await future
    assert x == 42

    # For stopping iteration:
    next_coro = anext(xs)
    future = asyncio.ensure_future(next_coro)
    c.future.cancel()

    # This should raise StopAsyncIteration
    try:
        await future
        assert False, "Should have raised StopAsyncIteration"
    except StopAsyncIteration:
        pass
