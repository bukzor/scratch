def capitalize(f):
	def cap_wrapper(self):
		return f(self).upper()
	return cap_wrapper

class CapitalizingClass(type):
	"""
	A CapitalizingClass knows that the output of some methods need
	capitalized.
	"""
	def __init__(cls, name, bases, dct):
		super(CapitalizingClass, cls).__init__(name, bases, dct)
		for funcname in cls.capitalize:
			func = getattr(cls, funcname)
			func = capitalize(func)
			setattr(cls, funcname, func)

class Base(object):
	__metaclass__ = CapitalizingClass
	capitalize = ['f']
	def f(self):
		return 'bar'

class Sub(Base):
	def f(self):
		return 'foo'

def main():
	print Sub().f()
	print Base().f()

if __name__ == '__main__':
	main()
