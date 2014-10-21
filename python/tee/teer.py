"""
Show a command's output in realtime and capture its outputs as strings,
without deadlocking or temporary files.
"""
import os
from subprocess import Popen, PIPE


def fdclosed(fd):
    """close a file descriptor, idempotently"""
    try:
        os.close(fd)
    except OSError as err:
        if err.errno == 9:  # bad file descriptor
            pass  # it's already closed: ok
        else:
            raise

class Pipe(object):
    """a convenience object, wrapping os.pipe()"""
    def __init__(self):
        self.read, self.write = os.pipe()

    def closed(self):
        """close both ends of the pipe. idempotent."""
        fdclosed(self.read)
        fdclosed(self.write)

    def readonly(self):
        """close the write end of the pipe. idempotent."""
        fdclosed(self.write)

    def writeonly(self):
        """close the read end of the pipe. idempotent."""
        fdclosed(self.read)


class Pty(Pipe):
    def __init__(self):  # pylint:disable=super-init-not-called
        self.read, self.write = os.openpty()


def run(cmd):
    """Run a command, showing its usual outputs in real time,
    and return its stdout and stderr as strings.

    No temporary files are used.
    """
    stdout_1 = Pty()  # libc uses full buffering for stdout if it doesn't see a tty
    stdout_2 = Pipe()
    stderr_1 = Pipe()
    stderr_2 = Pipe()
    # combined = Pipe()

    # deadlocks occur if we have any end of a pipe open more than once
    # best practice: close any unused pipes before spawn, closed used pipes after
    # use close_fds to close everything bug stdout, stderr
    outputter = Popen(
        cmd,
        stdout=stdout_1.write,
        stderr=stderr_1.write,
        close_fds=True,
    )

    ischild = not os.fork()
    if ischild:
        stdout_1.readonly()
        stdout_2.writeonly()
        stderr_1.closed()
        stderr_2.closed()
        proc = Popen(
            ('tee', '/dev/fd/%i' % stdout_2.write),
            stdin=stdout_1.read,
        )
        stdout_1.closed()
        stdout_2.closed()
        proc.wait()
        exit()

    ischild = not os.fork()
    if ischild:
        stdout_1.closed()
        stdout_2.closed()
        stderr_1.readonly()
        stderr_2.writeonly()
        proc = Popen(
            ('tee', '/dev/fd/%i' % stderr_2.write),
            stdin=stderr_1.read,
        )
        stderr_1.closed()
        stderr_2.closed()
        proc.wait()
        exit()

    stdout_1.closed()
    stdout_2.readonly()
    stderr_1.closed()
    stderr_2.readonly()

    # Popen.communicate only coordinates pipes from a single Popen object
    # I don't see any cleaner way to make use of the subprocess machinery -.-
    outputter.stdout = os.fdopen(stdout_2.read)
    outputter.stderr = os.fdopen(stderr_2.read)

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
