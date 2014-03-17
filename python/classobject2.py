
class Class(type):
    pass


class Object(Class):
    __metaclass__ = Class

    def __init__(cls, *args):
        #raise NotImplementedError('classobj init')
        pass

    def __new__(cls, name=None, bases=None, attrs=None):
        if name is bases is attrs is None:
            return cls.__instance()
        else:
            return super(Object, cls).__new__(cls, name, bases, attrs)

    def __call__(cls):
        return cls.__instance()

    @classmethod
    def __instance(cls):
        return Class.__new__(
            # Type of ObjectSubNew should be ObjectSub
            cls,
            cls.__name__ + 'New',
            (Class,),
            cls.__dict__.copy(),
        )

    @classmethod
    def __subclass(cls):
        #mcs = type(cls)
        return super(Class, cls).__new__(
            # Type of ObjectSubSub should be Class
            # Type of ObjectSub should be Class
            cls,  # When cls, cls.__call__ is used.
            cls.__name__ + 'Sub',
            # ObjectSub must subclass Object
            (cls,),
            cls.__dict__.copy(),
        )
