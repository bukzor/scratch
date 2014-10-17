"""
Show a command's output in realtime and capture its outputs as strings,
without deadlocking or temporary files.
"""
import os
from subprocess import Popen, PIPE


class Pipe(object):
    """a convenience object, wrapping os.pipe()"""
    def __init__(self):
        self.read, self.write = os.pipe()

    def close(self):
        """close both ends of the pipe"""
        os.close(self.read)
        os.close(self.write)


def run(cmd):
    """Run a command, showing its usual outputs in real time,
    and return its stdout and stderr as strings.

    No temporary files are used.
    """
    stdout = Pipe()
    stderr = Pipe()

    outputter = Popen(
        # without stdbuf, stdout doesn't show up till the cmd exits
        ('stdbuf', '-o0', '-e0') + cmd,
        stdout=stdout.write,
        stderr=stderr.write,
        # close_fds=True,  # how come this isn't necessary??
    )

    # deadlocks occur if any of the four below close's are deleted.
    stdoutter = Popen(
        ('tee', '/dev/fd/2'),
        stdin=stdout.read,
        stderr=PIPE,
        close_fds=True,
    )
    stdout.close()

    stderrter = Popen(
        ('tee', '/dev/fd/2'),
        stdin=stderr.read,
        stdout=PIPE,
        close_fds=True,
    )
    stderr.close()

    # Popen.communicate only coordinates pipes from a single Popen object
    # I don't see any cleaner way to make use of the subprocess machinery -.-
    outputter.stdout = stdoutter.stderr
    outputter.stderr = stderrter.stdout

    return outputter.communicate()


def demo():
    """Demonstrate that run() doesn't deadlock,
    even under worst-case conditions.
    """
    cmd = ('python', 'outputter.py')
    print 'CMD:', cmd
    stdout, stderr = run(cmd)

    print 'STDOUT:'
    print stderr.count('\n')

    print 'STDERR:'
    print stdout.count('\n')


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
LINES = 100
TIME = 4
WIDTH = 79
ERROR_RATIO = .50

for i in range(LINES):
    if random() > ERROR_RATIO:
        print('.' * WIDTH, file=stdout)
    else:
        print('$' * WIDTH, file=stderr)
    sleep(TIME / LINES)
''')


def main():
    """The entry point"""
    make_outputter()
    demo()


if __name__ == '__main__':
    exit(main())
