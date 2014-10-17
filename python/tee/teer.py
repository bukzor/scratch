"""
Show a command's output in realtime and capture its outputs as strings,
without deadlocking or temporary files.
"""
import os
from subprocess import Popen
from threading import Thread


class Tee(object):
    result = ''

    def __init__(self, out):
        self.out = out
        self.read, self.write = os.pipe()

        self.thread = Thread(target=self.tee)

    def start(self):
        os.close(self.write)
        self.thread.start()

    def join(self):
        self.thread.join()
        os.close(self.read)
        return self.result

    def tee(self):
        read = lambda: os.read(self.read, 1 << 12)
        for line in iter(read, b''):
            os.write(self.out, line)
            self.result += line

def run(cmd):
    """Run a command, showing its usual outputs in real time,
    and return its stdout and stderr as strings.

    No temporary files are used.
    """
    stdout = Tee(1)
    stderr = Tee(2)

    outputter = Popen(
        # without stdbuf, stdout doesn't show up till the cmd exits
        ('stdbuf', '-o0', '-e0') + cmd,
        stdout=stdout.write,
        stderr=stderr.write,
        # close_fds=True,  # how come this isn't necessary??
    )

    stdout.start()
    stderr.start()
    outputter.communicate()

    return stdout.join(), stderr.join()


def demo():
    """Demonstrate that run() doesn't deadlock,
    even under worst-case conditions.
    """
    cmd = ('python', 'outputter.py')
    print 'CMD:', cmd
    stdout, stderr = run(cmd)

    print 'STDOUT:'
    print stdout.count('\n')

    print 'STDERR:'
    print stderr.count('\n')


def make_outputter():
    """Create the the outputter.py script, for the demonstration."""
    with open('outputter.py', 'w') as outputter:
        outputter.write('''\
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
        char = '.'
        file = stdout
    else:
        char = '%'
        file = stderr

    for j in range(WIDTH):
        print(char, file=file, end='')
        sleep(TIME / LINES / WIDTH)
    print(file=file)
''')


def main():
    """The entry point"""
    make_outputter()
    demo()


if __name__ == '__main__':
    exit(main())
