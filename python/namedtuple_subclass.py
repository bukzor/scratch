from collections import namedtuple

PointBase = namedtuple('Point', 'x y')

class Point(PointBase):
	@property
	def radius(self):
		import pudb; pudb.set_trace()
		return sum(axis**2 for axis in self)**.5

class Point3D(Point):
	def __new__(cls, x, y, z=0):
		self = super(cls, Point3D).__new__(cls, x, y)
		self.z = z
		return self

p = Point3D(2, 3, 6)
print 'p.x =', p.x
print 'p.y =', p.y
print 'p.z =', p.z
print 'p.radius =', p.radius
