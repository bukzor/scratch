# pylint:disable=missing-docstring
class Class(type):
    def __new__(mcs, name, bases, attrs):
        try:
            base = super(Class, mcs).__new__(
                mcs,
                name + 'Class',
                mcs.__bases__,
                attrs,
            )
        except:
            from class2dot import class2dot

            print class2dot(mcs)
            raise

        try:
            return type.__new__(
                base,
                name + 'Object',
                bases,
                {},
            )
        except:
            from class2dot import class2dot

            print class2dot(base, *bases)
            raise


class Object(Class):
    __metaclass__ = Class

    def __init__(cls, *args):
        #raise NotImplementedError('classobj init')
        pass

    def __new__(cls, name=None, bases=None, attrs=None):
        if name is bases is attrs is None:
            return cls.__instance()
        else:
            return Class.__new__(cls, name, bases, attrs)

    def __call__(cls):
        return cls.__instance()

    @classmethod
    def __instance(cls):
        return Class.__new__(
            # Type of ObjectSubNew should be ObjectSub
            cls,
            cls.__name__ + 'New',
            (cls,),
            cls.__dict__.copy(),
        )
