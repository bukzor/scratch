#!/usr/bin/env python
import sys
port = int(sys.argv[1])

from socket import socket
s = socket()
s.bind(('', port))
print(s.getsockname())
