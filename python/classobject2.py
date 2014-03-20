# pylint:disable=missing-docstring

class Class(type):
    def __new__(mcs, name, bases, attrs):
        for base in bases:
            # TypeError: metaclass conflict:
            #    the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases

            assert issubclass(mcs, type(base)), (mcs, base, type(base))

        try:
            base = super(Class, mcs).__new__(
                mcs,
                name + 'Class',
                (mcs,),
                attrs,
            )
        except:
            from class2dot import class2dot
            print class2dot(mcs)
            raise

        return type.__new__(
            base,
            name + 'Object',
            bases,
            {},
        )


class Object(Class):
    __metaclass__ = Class

    def __init__(cls, *args):
        #raise NotImplementedError('classobj init')
        Class.__init__(cls, *args)

    def __new__(mcs, name=None, bases=None, attrs=None):
        if name is bases is attrs is None:
            return mcs.__instance('New')
        else:
            return Class.__new__(mcs, name, bases, attrs)

    def __call__(cls, name=None, bases=None, attrs=None):
        if name is bases is attrs is None:
            return cls.__instance('Call')
        else:
            return Class.__new__(cls, name, bases, attrs)

    def __instance(mcs, label):
        return Class.__new__(
            # Type of ObjectSubNew should be ObjectSub
            mcs,
            mcs.__name__ + label,
            (Class,),
            mcs.__dict__.copy(),
        )


def main():
    classes = []

    classes.append(Object()()())

    class subclass(Object): pass
    classes.append(subclass()())

    class subclass2(Object()): pass
    classes.append(subclass2())

    class subclass3(subclass): pass
    classes.append(subclass3())

    class subclass4(subclass2): pass
    classes.append(subclass4())

    class subclass5(subclass3()): pass
    classes.append(subclass5())

    from class2dot import class2dot
    print class2dot(*classes)

if __name__ == '__main__':
    exit(main()) 
