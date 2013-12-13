
class C(object):
	def __eq__(self, other):
		return self is other
	def __lt__(self, other):
		raise NotImplementedError("No sorting defined.")
	
c1 = C()
c2 = C()
c3 = C()

print sorted([c1, c2, c3])
