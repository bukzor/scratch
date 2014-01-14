# I0011: disabling locally
# C0301: line too long
# W0111: missing docstring
# C0103: invalid class name
# pylint:disable=I0011,C0301,C0111,C0103
from frozendict import FrozenDict as fdict

try:
    from buck.pprint import pformat
except ImportError:
    from pprint import pformat

def pudb():
    from pudb import set_trace
    set_trace()

class tokenType(type):
    children = ()
    properties = fdict()
    undefined = object()

    def __repr__(cls):
        return pformat(cls.__primitive__())

    @classmethod
    def __primitive__(mcs):
        # This is (so far) primarily to make the structure easily viewable for debugging.
        result = (mcs.__name__,)
        if mcs.children:
            result += tuple(mcs.children)
        if mcs.properties:
            result += (dict(mcs.properties),)
        return result

    def __eq__(cls, other):
        if isinstance(other, tokenType):
            return cls.__primitive__() == other.__primitive__()
        else:
            return False
    def __ne__(cls, other):
        if isinstance(other, tokenType):
            return cls.__primitive__() != other.__primitive__()
        else:
            return True
    def __len__(cls):
        return len(cls.children)
    def __iter__(cls):
        return iter(cls.children)

    @classmethod
    def copy(mcs, children=(), properties=None):
        # Make a copy, with altered children and/or properties attributes.
        attrs = {}
        if children:
            attrs['children'] = tuple(children)

        if properties:
            attrs['properties'] = fdict(mcs.properties).update(properties)
            attrs['properties'] = fdict(
                    (key, val)
                    for key, val in attrs['properties'].items()
                    if val is not token.undefined
            )

        mcs_copy = super(tokenType, mcs).__new__(
                # Inherit attributes of the copied class
                mcs,
                mcs.__name__,
                (mcs,),
                attrs,
        )
        return mcs_copy

    # Be immutable.
    def __setattr__(cls, key, value=None):
        raise TypeError("{name} objects are read-only".format(name=type(cls).__name__))
    def __delattr__(cls, key):
        raise TypeError("{name} objects are read-only".format(name=type(cls).__name__))


class token(tokenType):
    """The most generic token."""
    __metaclass__ = tokenType

    def __new__(mcs, *children, **properties):
        return mcs.copy(children, properties)

    def __init__(cls, *children, **properties):
        del children, properties
        # The `type` initializer takes quite different arguments.
        # SMELL: Replace the last three arguments with None and all tests still pass...
        super(token, cls).__init__(cls, cls.__name__, cls.__bases__, cls.__dict__)
