from __future__ import print_function
from __future__ import unicode_literals


def simple_read(fd):
    # this yields IOError:4 <fdopen>, on pypy+pty only
    from os import fdopen
    return fdopen(fd).read()

def read_loop(fd):
    # this is the only method that works under pypy
    from os import read
    result = []
    lastread = None
    while lastread != '':
        try:
            lastread = read(fd, 1024 * 1024)
        except OSError as err:
            if err.errno == 5:
                lastread = ''  # slave closed
            else:
                raise
        result.append(lastread)

    return ''.join(result)


def pipe_output(read, write):
    from subprocess import Popen
    process = Popen(
        ('echo', 'hi', 'there!'),
        stdout=write,
    )
    from os import close
    close(write)

    result = read_loop(read)
    close(read)
    process.wait()

    # python3 somehow does universal-newlines on file descriptors
    # while python2 doesn't.
    # This replace normalizes the two.
    return result.replace('\r\n', '\n')


def test_pty():
    from os import openpty
    read, write = openpty()

    out = pipe_output(read, write)

    assert out == 'hi there!\n', repr(out)

    return 'pty works'


def test_pipe():
    from os import pipe
    read, write = pipe()

    out = pipe_output(read, write)

    assert out == 'hi there!\n', repr(out)

    return 'pipe works'


def main():
    print(test_pipe())
    print(test_pty())


if __name__ == '__main__':
    exit(main())
