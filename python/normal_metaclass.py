# I0011: disabling locally
# C0301: line too long
# W0111: missing docstring
# R0903: too few methods
# pylint:disable=I0011,C0301,C0111,R0903

def showargs(note, cls, *args):
    print '%s %r:' % (note, cls.__name__)
    for i, arg in enumerate(args, 1):
        print '   %i) %r' % (i, arg)

class MyBaseType(type):
    def __new__(mcs, name, bases, attrs):
        showargs('New', MyBaseType, mcs, name, bases, attrs)
        cls = super(MyBaseType, mcs).__new__(mcs, name, bases, attrs)
        return cls

    def __init__(cls, name, bases, attrs):
        showargs('Init', MyBaseType, cls, name, bases, attrs)
        super(MyBaseType, cls).__init__(name, bases, attrs)

class MySubTypeA(MyBaseType):
    def __new__(mcs, name, bases, attrs):
        showargs('New', MySubTypeA, mcs, name, bases, attrs)
        cls = super(MySubTypeA, mcs).__new__(mcs, name, bases, attrs)
        return cls

    def __init__(cls, name, bases, attrs):
        showargs('Init', MySubTypeA, cls, name, bases, attrs)
        super(MySubTypeA, cls).__init__(name, bases, attrs)

class MySubTypeB(MyBaseType):
    def __new__(mcs, name, bases, attrs):
        showargs('New', MySubTypeB, mcs, name, bases, attrs)
        cls = super(MySubTypeB, mcs).__new__(mcs, name, bases, attrs)
        return cls

    def __init__(cls, name, bases, attrs):
        showargs('Init', MySubTypeB, cls, name, bases, attrs)
        super(MySubTypeB, cls).__init__(name, bases, attrs)

class MyType(MySubTypeA, MySubTypeB):
    def __new__(mcs, name, bases, attrs):
        showargs('New', MyType, mcs, name, bases, attrs)
        cls = super(MyType, mcs).__new__(mcs, name, bases, attrs)
        return cls

    def __init__(cls, name, bases, attrs):
        showargs('Init', MyType, cls, name, bases, attrs)
        super(MyType, cls).__init__(name, bases, attrs)


class MyObject(object):
    __metaclass__ = MyType
