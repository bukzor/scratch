#!/usr/bin/env python
import sys
port = int(sys.argv[1])

import socket
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', port))
print(s.getsockname())
