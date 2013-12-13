from primitive import primitive

try:
	from buck.pprint import pprint, pformat
	pprint, pformat # pyflakes, wat
except ImportError:
	from pprint import pprint, pformat
	pprint, pformat # pyflakes, wat

class tokenMeta(type):
	#def __repr__(self):
		#return '<TOKEN %#05x>' % ((id(self) % id(tokenMeta))>>3)
	children = ()
	properties = {}

	def __repr__(self):
		return pformat(primitive(self))

	def __primitive__(self):
		# This is (so far) primarily to make the structure easily viewable for debugging.
		result = (type(self),)
		if self.children:
			result += tuple(self.children)
		if self.properties:
			result += (self.properties,)
		return result


class token(tokenMeta):
	__metaclass__ = tokenMeta

	def __new__(cls, *children, **properties):
		# Make a copy, with altered children / properties
		self = super(tokenMeta, cls).__new__(
				cls,
				cls.__name__,
				cls.__bases__,
				dict(
					children=children,
					properties=properties,
				),
		)
		return self

	def __init__(cls, *children, **properties):
		pass
	
	# Be immutable.
	def __setattr__(self, key, value=None):
		raise TypeError("{name} objects are read-only".format(name=type(self).__name__))
	def __delattr__(self, key):
		raise TypeError("{name} objects are read-only".format(name=type(self).__name__))


class goat(token): pass


token2 = token(
		goat,
		goat,
)

import pudb; pudb.set_trace()
print 'token1:', token
print token.__bases__
print 'token2:', token2
print token2.__bases__
