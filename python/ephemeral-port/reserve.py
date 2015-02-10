#!/usr/bin/env python
from socket import socket, error
from socket import SOL_SOCKET, SO_REUSEADDR

s = socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(('', 0))
s.listen(0)

sockname = s.getsockname()

s2 = socket()
s2.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s2.connect(sockname)

s3, sockname2 = s.accept()
s3.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

s3.setblocking(0)
try:
    s3.recv(0)
except error:
    pass

print(sockname2[1])
