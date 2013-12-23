try:
	from buck.pprint import pprint, pformat
	pprint, pformat # pyflakes, wat
except ImportError:
	from pprint import pprint, pformat
	pprint, pformat # pyflakes, wat

class tokenType(type):
	children = ()
	properties = {}

	def __repr__(cls):
		return pformat(cls.__primitive__())

	@classmethod
	def __primitive__(cls):
		# This is (so far) primarily to make the structure easily viewable for debugging.
		result = (cls.__name__,)
		if cls.children:
			result += tuple(cls.children)
		if cls.properties:
			result += (cls.properties,)
		return result

	def __eq__(cls, other):
		return cls.__primitive__() == other.__primitive__()

class token(tokenType):
	__metaclass__ = tokenType

	def __new__(cls, *children, **properties):
		# Make a copy, with altered children / properties
		if not children:
			children = cls.children

		if properties:
			tmp = properties
			properties = cls.properties.copy()
			properties.update(tmp)
			del tmp
		else:
			properties = cls.properties

		cls_copy = super(token, cls).__new__(
				type(cls),
				cls.__name__,
				cls.__bases__,
				dict(
					children=children,
					properties=properties,
				),
		)
		return cls_copy

	def __init__(cls, *children, **properties):
		pass
	
	# Be immutable.
	def __setattr__(self, key, value=None):
		raise TypeError("{name} objects are read-only".format(name=type(self).__name__))
	def __delattr__(self, key):
		raise TypeError("{name} objects are read-only".format(name=type(self).__name__))


class goat(token):
	pass


token2 = token(
		goat(a=1),
		goat(b=2),
)

print 'token1:', token
print token.__bases__
print 'token2:', token2
print token2.__bases__

assert issubclass(goat, token)
assert issubclass(goat(), token)

#import pudb; pudb.set_trace()
assert goat == goat()
