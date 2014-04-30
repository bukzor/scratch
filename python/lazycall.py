from __future__ import print_function


class LazyCall(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __get__(self, obj, cls):
        print('__get__')
        result = self.func(*self.args, **self.kwargs)

        for o in (obj, cls):
            attrs = vars(o)
            for attr, val in attrs.items():
                if val is self:
                    print('replacing %s on %s' % (attr, o))
                    setattr(o, attr, result)

        return result


class DescriptoredObject(object):

    def __getattribute__(self, attr):
        val = object.__getattribute__(self, attr)

        # This is standard __getattribute__ behavior except at the object level
        if hasattr(val, '__get__'):
            return val.__get__(self, type(self))
        else:
            return val


class MyClass(DescriptoredObject):
    def __init__(self, x):
        self.x = x


def lazyrand():
    import random
    return LazyCall(random.randint, 1, 9001)


class MyClass2(object):
    y = lazyrand()


def main():
    m = MyClass(lazyrand())
    print(m.x)
    print(m.x)

    m = MyClass(lazyrand())
    print(m.x)
    print(m.x)

    m = MyClass(lazyrand())
    print(m.x)
    print(m.x)

    m = MyClass2()
    print(m.y)
    print(m.y)
    print(m.y)
    print(m.y)

    m = MyClass2()
    print(m.y)


if __name__ == '__main__':
    exit(main())
