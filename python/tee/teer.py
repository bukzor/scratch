"""
Show a command's output in realtime and capture its outputs as strings,
without deadlocking or temporary files.
"""
from __future__ import print_function

import os
from subprocess import Popen

PY3 = (str is not bytes)


# posix standard file descriptors
STDIN, STDOUT, STDERR = range(3)

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
        if PY3:
            print('PY3')
            # emulate old os.pipe
            os.set_inheritable(self.read, True)
            os.set_inheritable(self.write, True)

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
    """Represent a pty as a pipe"""
    def __init__(self):  # pylint:disable=super-init-not-called
        self.read, self.write = os.openpty()


def tee(read_fd, write_fd, *other_fds):
    """send output from read_fd to write_fd,
    but also copy it to each of other_fds
    """
    ischild = not os.fork()
    if ischild:
        os.dup2(read_fd, STDIN)
        os.dup2(write_fd, STDOUT)
        os.execvp(
            'tee',
            ('tee', ) + tuple(
                '/dev/fd/%i' % fd
                for fd in other_fds
            )
        )  # never returns
    os.close(read_fd)


def _communicate_with_select(read_set):
    """stolen from stdlib subprocess.Popen._communicate_with_select

    changes:
        arbitrary-length list of fds as input
        deleted stdin/input support
    """
    import select
    import errno

    orig_read_set = read_set
    read_set = list(read_set)
    result = {}
    for fd in read_set:
        result[fd] = []

    while read_set:
        try:
            readable, _, _ = select.select(read_set, [], [])
        except select.error as error:
            if error.args[0] == errno.EINTR:
                continue
            raise

        for fd in readable:
            data = os.read(fd, 1024)
            if data == b"":
                os.close(fd)
                read_set.remove(fd)
            result[fd].append(data)

    return tuple(
        b''.join(result[fd])
        for fd in orig_read_set
    )


def run(cmd):
    """Run a command, showing its usual outputs in real time,
    and return its stdout and stderr as strings.

    No temporary files are used.
    """
    stdout_orig = Pty()  # libc uses full buffering for stdout if it doesn't see a tty
    stderr_orig = Pipe()

    # deadlocks occur if we have any write-end of a pipe open more than once
    # best practice: close any used write pipes just after spawn
    outputter = Popen(
        cmd,
        stdout=stdout_orig.write,
        stderr=stderr_orig.write,
        close_fds=False,  # default changed to True in py3
    )
    stdout_orig.readonly()  # deadlock otherwise
    stderr_orig.readonly()  # deadlock otherwise

    # start one tee each on the original stdout and stderr
    # writing each to three places:
    #    1. the original destination
    #    2. a pipe just for that one stream
    #    3. a pipe that shows the combined output
    stdout_teed = Pipe()
    stderr_teed = Pipe()
    combined = Pipe()

    tee(stdout_orig.read, STDOUT, stdout_teed.write, combined.write)
    tee(stderr_orig.read, STDERR, stderr_teed.write, combined.write)
    stdout_teed.readonly()  # deadlock otherwise
    stderr_teed.readonly()  # deadlock otherwise
    combined.readonly()  # deadlock otherwise

    # communicate closes fds when it's done with them
    result = _communicate_with_select((stdout_teed.read, stderr_teed.read, combined.read))

    # clean up left-over processes and pipes:
    outputter.wait()
    stdout_teed.closed()
    stderr_teed.closed()
    combined.closed()

    return result


def demo():
    """Demonstrate that run() doesn't deadlock,
    even under worst-case conditions.
    """
    from sys import executable
    cmd = (executable, 'outputter.py')
    print('CMD:', cmd)
    stdout, stderr, combined = run(cmd)

    print('STDOUT:')
    print(stdout.count(b'\n'))

    print('STDERR:')
    print(stderr.count(b'\n'))

    print('COMBINED:')
    print(combined.count(b'\n'))


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
''')


def main():
    """The entry point"""
    make_outputter()
    demo()


if __name__ == '__main__':
    exit(main())
