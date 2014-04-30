# pylint:disable=missing-docstring

def makeobject(mcs):
    bases = (type,)
    #return ''
    try:
        return mcs('%s-object' % mcs.__name__, bases, {})
    except TypeError as error:
        return '''\
%s failed.
%s
Metaclass: %s
Metaclass superclasses: %s
Superclass's metaclasses: %s
''' % (
            mcs.__name__,
            error,
            mcs,
            mcs.mro(mcs),
            tuple(type(base) for base in bases),
        )


class r0c0(type):
    @property
    def r0c0(self):
        return 'r0c0-property'
print r0c0.r0c0

r0c0Object = makeobject(r0c0)
print r0c0Object.r0c0

class r1c0(r0c0):
    __metaclass__ = r0c0
r1c0Object = makeobject(r1c0)

class r2c0(r1c0):
    __metaclass__ = r1c0
r2c0Object = makeobject(r2c0)


class r0c1(r0c0):
    __metaclass__ = r0c0
r0c1Object = makeobject(r0c1)

class r1c1(r0c1):
    __metaclass__ = r1c0
r1c1Object = makeobject(r1c1)

class r2c1(r1c1):
    __metaclass__ = r2c0
r2c1Object = makeobject(r2c1)


class r0c2(r0c1):
    __metaclass__ = r0c1
r0c2Object = makeobject(r0c2)

class r1c2(r0c2):
    __metaclass__ = r1c1
r1c2Object = makeobject(r1c2)

class r2c2(r1c2):
    __metaclass__ = r2c1
r2c2Object = makeobject(r2c2)
