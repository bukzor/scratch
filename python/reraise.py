from contextlib import contextmanager
@contextmanager
def helpful_info():
	try:
		yield
	except Exception as e:
		class CloneException(Exception): pass
		CloneException.__name__ = type(e).__name__
		CloneException.__module___ = type(e).__module__
		helpful_message = 'helpful info!\n\n%s' % e
		import sys
		raise CloneException, helpful_message, sys.exc_traceback


class BadException(Exception):
	def __str__(self):
		return 'wat.'

with helpful_info():
	raise BadException('fooooo')

result = """
Traceback (most recent call last):
  File "re_raise.py", line 20, in <module>
    raise BadException('fooooo')
  File "/usr/lib64/python2.6/contextlib.py", line 34, in __exit__
    self.gen.throw(type, value, traceback)
  File "re_raise.py", line 5, in helpful_info
    yield
  File "re_raise.py", line 20, in <module>
    raise BadException('fooooo')
__main__.BadException: wat.

helpful info!
"""
