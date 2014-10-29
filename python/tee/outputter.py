from __future__ import print_function
from __future__ import division
from sys import stdout, stderr
from time import sleep
from random import random

# system should not deadlock for any given value of these parameters.
LINES = 1000
TIME = 2
WIDTH = 179
ERROR_RATIO = .40

PY3 = (str is not bytes)
if PY3:
    # emulate the old, less-buffered print
    orig_print = print
    def print(*args, **kwargs):
        kwargs.setdefault('flush', True)
        orig_print(*args, **kwargs)

for i in range(LINES):
    if random() > ERROR_RATIO:
        char = '.'
        file = stdout
    else:
        char = '%'
        file = stderr

    for j in range(WIDTH):
        print(char, file=file, end='')
        sleep(TIME / LINES / WIDTH)
    print(file=file)
print('EOF:stderr', file=stderr)
print('EOF:stdout', file=stdout)
