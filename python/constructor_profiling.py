class Option0(object):
	__slots__ = ['a', 'b', 'c', 'd', 'e']

	def __init__(self, a, b, c, d, e):
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.e = e

class Option0p1(object):
	def __init__(self, a, b, c, d, e):
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.e = e

class Option1(object):
	__slots__ = ['a', 'b', 'c', 'd', 'e']

	def __init__(self, a, b, c, d, e):
		setattr = object.__setattr__
		setattr(self, 'a', a)
		setattr(self, 'b', b)
		setattr(self, 'c', c)
		setattr(self, 'd', d)
		setattr(self, 'e', e)

class Option2(object):
	__slots__ = ['a', 'b', 'c', 'd', 'e']

	def __init__(self, a, b, c, d, e):
		setattr(self, 'a', a)
		setattr(self, 'b', b)
		setattr(self, 'c', c)
		setattr(self, 'd', d)
		setattr(self, 'e', e)

class Option3p0(object):
	def __init__(self, a, b, c, d, e):
		vals = {'a': a, 'b': b, 'c': c, 'd':d, 'e':e}
		self.__dict__ = vals

class Option3p1(object):
	def __init__(self, a, b, c, d, e):
		vals = dict(a=a, b=b, c=c, d=d, e=e)
		self.__dict__ = vals

class Option3p2(object):
	def __init__(self, a, b, c, d, e):
		self.__dict__ = dict(a=a, b=b, c=c, d=d, e=e)

class Option3p3(object):
	def __init__(self, a, b, c, d, e):
		self.__dict__ = {'a': a, 'b': b, 'c': c, 'd':d, 'e':e}

class Option4(object):
	def __init__(self, a, b, c, d, e):
		vals = dict(a=a, b=b, c=c, d=d, e=e)
		self.__dict__.update(vals)

class Option5(object):
	def __init__(self, a, b, c, d, e):
		vals = dict(a=a, b=b, c=c, d=d, e=e)
		self.__dict__.update(**vals)

class Option6(object):
	def __init__(self, a, b, c, d, e):
		vals = {'a': a, 'b': b, 'c': c, 'd':d, 'e':e}
		self.__dict__.update(**vals)

class Option7(object):
	def __init__(self, a, b, c, d, e):
		self.__dict__.update(a=a, b=b, c=c, d=d, e=e)

def profile(cls):
	print cls.__name__,
	from time import time
	i = 1000000

	obj = cls(1,2,3,4,5)
	assert obj.a == 1
	assert obj.b == 2
	assert obj.c == 3
	assert obj.d == 4
	assert obj.e == 5

	start = time()
	while i:
		cls(1,2,3,4,5)
		i -= 1
	end = time()
	print end - start

def main():
	for cls in (
			Option0,
			Option0p1,
			Option1,
			Option2,
			Option3p0,
			Option3p1,
			Option3p2,
			Option3p3,
			Option4,
			Option5,
			Option6,
			Option7,
		):
		profile(cls)

if __name__ == '__main__':
	main()



