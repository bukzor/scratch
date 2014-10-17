"""This doesn't work."""
import os
from subprocess import Popen

new_stdout = os.dup(1)

outputter = Popen(
    # without stdbuf, stdout doesn't show up till the cmd exits
    ('echo', 'hello, world!'),
    close_fds=True,
)

print outputter.communicate()

print 'STDOUT:', os.fdopen(new_stdout).read()
