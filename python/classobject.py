"""Blur the line between class and object."""

class Class(type):
    def __new__(mcs, name, bases, attrs):
        print 'Class.__new__:', mcs, name, bases, attrs
        print
        for base in bases:
            # TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases

            assert issubclass(mcs, type(base)), (mcs, base, type(base))

        # This is (nearly) the default behavior for a metaclass.
        cls = type.__new__(
            mcs,
            name + 'Class',
            bases,
            attrs,
        )
        return cls

        # We instantiate the class we would normally return.
        # This allows properties and methods to be useful in a class-only world.
        return type.__new__(
            cls,
            name + 'Object',
            bases,
            {},
        )

class Object(Class):
    __metaclass__ = Class

    @property
    def foo(self):
        return 'foo'

    def __call__(cls, name=None, bases=None, attrs=None):
        return cls.__new__(name, bases, attrs)

    def __init__(cls, *args):
        pass

    def __new__(cls, name=None, bases=None, attrs=None):
        mcs = type(cls)

        if None not in (name, bases, attrs):
            # Make a new class quite similar to this one, but with different attrs.
            tmp = attrs
            attrs = cls.__dict__.copy()
            attrs.update(tmp)

            mcs = type(cls)
            return Class.__new__(
                mcs,
                name + 'New',
                bases,
                attrs,
            )


        return Class.__new__(
            cls,
            cls.__name__ + 'Copy',
            (cls,),
            cls.__dict__.copy(),
        )

def mro(cls):
    return [c.__name__ for c in type.mro(cls)]


def main():
    print Object
    print 'Superclasses:', mro(Object)
    assert mro(Object) == ['ObjectObject', 'Class', 'type', 'object']
    print 'Metaclasses:', mro(type(Object))
    #assert mro(type(Object)) == ['ObjectClass', 'type', 'object']
    print type(Object)
    assert issubclass(Object, Class), (type(Object), Class)
    print Object.foo
    assert Object.foo == 'foo'
    print

    #import pudb; pudb.set_trace()
    O = Object()
    print mro(O)
    assert mro(O) == ['ObjectObjectCopyObject', 'ObjectClass', 'Class', 'type', 'object']
    assert isinstance(O, Class)
    print type(O)
    print mro(type(O))
    assert mro(type(O)) == ['ObjectObjectCopyClass', 'ObjectClass', 'Class', 'type', 'object']
    assert issubclass(O, Object), (type(O), Object)
    print O.foo
    assert O.foo == 'foo'
    print type(type(O))
    assert type(type(O)) is type(Object)
    print


    #import pudb; pudb.set_trace()
    class B(O):
        @property
        def foo(self):
            return 'bar'

    print B
    assert mro(B) == ['BNewObject', 'ObjectObject', 'Class', 'type', 'object'], mro(B)
    assert isinstance(B, Class)
    print type(B)
    assert issubclass(B, Object)
    print mro(type(B))
    assert mro(type(B)) == ['BNewClass', 'ObjectClass', 'Class', 'type', 'object']
    assert isinstance(type(B), Class)
    print B.foo
    assert type(type(B)) is type(Object), (type(B), Object)
    print


    O = B()
    print O
    assert isinstance(O, Class)
    assert issubclass(O, B)
    print type(O)
    assert isinstance(type(O), Class)
    assert isinstance(O, type(B))
    print O.foo
    assert type(type(O)) is type(B)
    print


if __name__ == '__main__':
    exit(main())
