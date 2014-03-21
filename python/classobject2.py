# pylint:disable=missing-docstring
class Class(type):
    def __new__(mcs, name, bases, attrs):
        return super(Class, mcs).__new__(
            mcs,
            name + 'Class',
            bases,
            attrs,
        )

    def __getattribute__(cls, attr):
        "Emulate type_getattro() in Objects/typeobject.c"
        val = type.__getattribute__(cls, attr)
        if hasattr(val, '__get__'):
            return val.__get__(None, type(cls))
        else:
            return val


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

    def __call__(cls):
        return cls.__instance()

    @classmethod
    def __instance(mcs):
        return Class.__new__(
            # Type of ObjectSubNew should be ObjectSub
            mcs,
            mcs.__name__ + 'New',
            (mcs,),
            mcs.__dict__.copy(),
        )
