
class Class(type):
    pass


class Object(Class):
    __metaclass__ = Class

    def __init__(cls, *args):
        #raise NotImplementedError('classobj init')
        pass

    def __new__(cls, name=None, bases=None, attrs=None):
        mcs = type(cls)
        if name is bases is attrs is None:
            return super(Object, cls).__new__(
                cls,
                cls.__name__ + 'Copy',
                (cls,),
                cls.__dict__.copy(),
            )
        else:
            raise NotImplementedError('classobj new')

    def __call__(cls, name=None, bases=None, attrs=None):

        if name is bases is attrs is None:
            return Class.__new__(
                cls,
                cls.__name__ + 'New',
                (Class,),
                cls.__dict__.copy(),
            )
        else:
            raise NotImplementedError('classobj call')
