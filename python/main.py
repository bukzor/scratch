
import sys

# Three possibile strategies for getting a fresh import.
def strat4():
	del sys.modules['sub']

from sub import foo
foo()

from sub import bar
bar()

strat4()
