from __future__ import print_function
from __future__ import division
from sys import stdout, stderr
from time import sleep
from random import random

# system should not deadlock for any given value of these parameters.
LINES = 10
TIME = 1
WIDTH = 79
ERROR_RATIO = .50

for i in range(LINES):
    if random() > ERROR_RATIO:
        print('.' * WIDTH, file=stdout)
    else:
        print('$' * WIDTH, file=stderr)
    sleep(TIME / LINES)
