# I0011: disabling locally
# C0301: line too long
# W0111: missing docstring
# C0103: invalid class name
# pylint:disable=I0011,C0301,C0111,C0103
try:
    from buck.pprint import pformat
except ImportError:
    from pprint import pformat

def pudb():
    from pudb import set_trace
    set_trace()

class tokenType(type):
    children = ()
    properties = {}

    def __repr__(cls):
        return pformat(cls.__primitive__())

    @classmethod
    def __primitive__(mcs):
        # This is (so far) primarily to make the structure easily viewable for debugging.
        result = (mcs.__name__,)
        if mcs.children:
            result += tuple(mcs.children)
        if mcs.properties:
            result += (mcs.properties,)
        return result

    def __eq__(cls, other):
        return cls.__primitive__() == other.__primitive__()
    def __ne__(cls, other):
        return cls.__primitive__() != other.__primitive__()
    def __len__(cls):
        return len(cls.children)
    def __iter__(cls):
        return iter(cls.children)

    # Be immutable.
    def __setattr__(cls, key, value=None):
        raise TypeError("{name} objects are read-only".format(name=type(cls).__name__))
    def __delattr__(cls, key):
        raise TypeError("{name} objects are read-only".format(name=type(cls).__name__))


class token(tokenType):
    __metaclass__ = tokenType

    def __new__(mcs, *children, **properties):
        # Make a copy, with altered children and/or properties attributes.
        attrs = {}
        if children:
            attrs['children'] = children

        if properties:
            attrs['properties'] = mcs.properties.copy()
            attrs['properties'].update(properties)

        # Seems like a good idea. Makes things worse.
        #if not attrs:
            ## trivial copy
            #return mcs

        # maybe? doesn't seem to work.
        #mcs_copy2 = super(token, mcs).__new__(
                ## Inherit attributes of the copied class
                #type(mcs),
                #mcs.__name__,
                #mcs.__bases__,
                #attrs,
        #)
        mcs_copy = super(token, mcs).__new__(
                # Inherit attributes of the copied class
                mcs,
                mcs.__name__,
                (mcs,),
                attrs,
        )
        return mcs_copy

    def __init__(cls, *children, **properties):
        del children, properties
        # The `type` initializer takes quite different arguments.
        # SMELL: Replace these three values with None and all tests still pass...
        super(token, cls).__init__(cls, cls.__name__, cls.__bases__, cls.__dict__)

    # Be immutable.
    def __setattr__(cls, key, value=None):
        raise TypeError("{name} objects are read-only".format(name=type(cls).__name__))
    def __delattr__(cls, key):
        raise TypeError("{name} objects are read-only".format(name=type(cls).__name__))
