from __future__ import print_function

from os import openpty
read, write = openpty()

from subprocess import Popen
proc = Popen(
    ('echo', 'ok'),
    stdout=write,
    close_fds=True,
)

from os import fdopen
fdopen(write, 'w').close()
with fdopen(read) as stdout:
    print('STDOUT', stdout.read())

print('exit code:', proc.wait())


output = '''
$ python2.6 pty.py
STDOUT ok
exit code: 0

$ python2.7 pty.py
STDOUT ok
exit code: 0

$ python3.3 pty.py
STDOUT ok
exit code: 0

$ python3.4 pty.py
Traceback (most recent call last):
  File "pty.py", line 16, in <module>
    print('STDOUT', stdout.read())
OSError: [Errno 5] Input/output error
'''
