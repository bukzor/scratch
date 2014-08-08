from __future__ import division

class PropertiedClass(type):
    """The class of classes which have @property's that work"""

    def __getattribute__(cls, attr):
        """Twiddle descriptor behavior slightly, so that classes have useful properties and methods."""
        print 'DEBUG: Getting', cls, attr
        getattribute = object.__getattribute__
        val = getattribute(cls, attr)

        # This is the standard __getattribute__ behavior of objects.
        # It's different to also have this behavior for classes.
        if hasattr(val, '__get__'):
            print 'DEBUG: has __get__'
            return val.__get__(cls, type(cls))
        else:
            print 'DEBUG: plain-old value'
            return val



class MyObject(object):
    __metaclass__ = PropertiedClass
    x = 2
    y = 3
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mult(self):
        return self.x * self.y

    @property
    def pmult(self):
        return self.x * self.y

    @classmethod
    def cmult(self):
        return self.x * self.y

    @staticmethod
    def smult():
        return MyObject.x * MyObject.y


print MyObject.mult()
print MyObject.pmult
#print MyObject.cmult()
print MyObject.smult()

o = MyObject(3, 5)
print o.mult()
print o.pmult
print o.cmult()
print o.smult()

class MyObject2(MyObject):
    # override property with plain-old data
    pmult = 7

print MyObject2.pmult
print MyObject2(2, 2).pmult


class MyClass(type):
    __metaclass__ = PropertiedClass

    def __new__(mcs, *args):
        print '__new__ args:', mcs, args
        return super(MyClass, mcs).__new__(mcs, *args)

class MyObject3(object):
    __metaclass__ = MyClass


o3 = MyObject3()
print o3
