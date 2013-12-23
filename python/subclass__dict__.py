
from ordereddict import OrderedDict


class MyObject(object):
	def __init__(self):
		self.__dict__ = OrderedDict()
		self.x = 1
		self.y = 2

print 1
m = MyObject()
print 2

for attr, val in m.__dict__.items():
	print attr, val
print 3
print 'm =', m
print 'm.x =', m.x
print 'm.__dict__ =', m.__dict__
print 'type(m.__dict__) =', type(m.__dict__)
exit()

class ImmutableError(TypeError): pass
	
class imdict(dict):
    def __hash__(self):
        return id(self)

    def _immutable(self, *args, **kws):
        raise ImmutableError('object is immutable')

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear       = _immutable
    update      = _immutable
    setdefault  = _immutable
    pop         = _immutable
    popitem     = _immutable


imd = imdict()
try:
	imd['a'] = 2
except ImmutableError:
	print 'imdict is immutable'

print 'm =', m
print 'm.x =', m.x
print 'm.__dict__ =', m.__dict__
print 'type(m.__dict__) =', type(m.__dict__)
try:
	m.__dict__['x'] = 3
except ImmutableError:
	print 'm.__dict__ is immutable.'
	print '... or is it ???'

m.x = 2
print 'm.x =', m.x
print 'm.__dict__ =', m.__dict__
print 'type(m.__dict__) =', type(m.__dict__)
