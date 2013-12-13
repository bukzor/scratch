from warnings import simplefilter, warn

simplefilter('error')

try:
	warn('foo')
	warning = None
except Warning, warning:
	pass

assert warning, warning
