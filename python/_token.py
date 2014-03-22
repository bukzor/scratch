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

    def copy(mcs, children=(), properties=None):
        # Make a copy, with altered children and/or properties attributes.
        attrs = vars(mcs).copy()

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
                (token,),
                attrs,
        )
        return mcs_copy

    # Be immutable.
    def __setattr__(cls, key, value=None):
        raise TypeError("{name} objects are read-only".format(name=type(cls).__name__))
    def __delattr__(cls, key):
        raise TypeError("{name} objects are read-only".format(name=type(cls).__name__))

    def __getattribute__(cls, attr):
        """Emulate type_getattro() in Objects/typeobject.c,
        except descriptors can be bound to classes too.
        """
        if attr == '__new__':
            val = type.__getattribute__(cls, attr)
            # python specifies type.__new__ as a special case. sadface.
            # Otherwise you get the metaclass as the first *two* arguments.
            result = val.__get__(None, type(cls))
        else:
            val = object.__getattribute__(cls, attr)
            if hasattr(val, '__get__'):
                result = val.__get__(cls, type(cls))
            else:
                result = val
        return result


class token(tokenType):
    """The most generic token."""
    __metaclass__ = tokenType

    def __new__(mcs, *children, **properties):
        if (
                not properties and
                len(children) == 3 and
                type(children[0]) is str and
                type(children[1]) is tuple and
                type(children[2]) is dict
        ):
            # used as the metaclass of a class
            return super(token, mcs).__new__(mcs, *children)
        else:
            # instantiated, like a plain-old object.
            return mcs.copy(children, properties)

    def __init__(cls, *children, **properties):
        # The `type` initializer takes quite different arguments.
        # type.__init__ is a noop as far as I can tell, but it makes pylint happy.
        del children, properties
        super(token, cls).__init__(cls, cls.__name__, cls.__bases__, cls.__dict__)
