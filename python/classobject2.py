# pylint:disable=missing-docstring
class Class(type):
    def __getattribute__(cls, attr):
        """Emulate type_getattro() in Objects/typeobject.c,
        except descriptors can be bound to classes too.
        """
        val = type.__getattribute__(cls, attr)
        if hasattr(val, '__get__'):
            if attr == '__new__':
                # python specifies type.__new__ as a special case. sadface.
                # Otherwise you get the metaclass as the first *two* arguments.
                result = val.__get__(None, type(cls))
            else:
                result = val.__get__(cls, type(cls))
        else:
            result = val
        return result


class Object(Class):
    __metaclass__ = Class

    def __init__(cls, *args):
        del args
        # type.__init__ is a noop as far as I can tell, but it makes pylint happy.
        super(Object, cls).__init__(cls, None, None, None)

    def __new__(mcs, name=None, bases=None, attrs=None):
        if name is bases is attrs is None:
            return mcs.__instance()
        else:
            return super(Object, mcs).__new__(mcs, name, bases, attrs)

    @classmethod
    def __instance(mcs):
        """Create a new class, very much like this one, but with different attr."""
        return super(Object, mcs).__new__(
            mcs,
            mcs.__name__,
            (Object,),
            mcs.__dict__.copy(),
        )
