"""A script that works :)"""
# Necessary for side-effects only.
import big_package.all_the_things as x
print x
del x
# End side-effects.

import big_package.thing2 as t2
print t2

print t2.THING2
