class Immutable(object):
    # Be immutable: we have no attributes.
    # This gives identical behavior to setattr/delattr/.__dict__ on a plain-old dict.
    def __noattr(self, attr='__dict__', dummy_value=None):
        """Provide a good error message on attempts to mutate this object."""
        clsname = type(self).__name__
        raise AttributeError("{clsname!r} object has no attribute {attr!r}".format(
            clsname=clsname, attr=attr,
        ))
    __setattr__ = __delattr__ = __noattr
    __dict__ = property(__noattr)


class ImmutableClass(Immutable, type):
    pass

class ImmutableObject(Immutable, object):
    __metaclass__ = ImmutableClass


imm = ImmutableObject

del Immutable, ImmutableClass, ImmutableObject
