# pylint:disable=missing-docstring
class Class(type):
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


class Object(Class):
    __metaclass__ = Class

    def __new__(mcs, name=None, bases=None, attrs=None):
        if name is bases is attrs is None:
            # Instantiated, like a normal class.
            # Create a new class, very much like this one, but with different attrs.
            name = mcs.__name__
            bases = (Object,)
            attrs = mcs.__dict__.copy()

        return super(Object, mcs).__new__(mcs, name, bases, attrs)

    def __init__(cls, *args):
        del args
        # type.__init__ is a noop as far as I can tell, but it makes pylint happy.
        super(Object, cls).__init__(cls, None, None, None)
