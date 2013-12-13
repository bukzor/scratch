#!/usr/bin/env python
import mock
import sys

class herp:
    class derp:
        foo = 'bar'


with mock.patch.dict(
    sys.modules,
    {
        'herp': herp,
        'herp.derp': herp.derp,
    }
):
    import herp.derp
    # prints bar
    print herp.derp.foo
