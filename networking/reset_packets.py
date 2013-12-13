import SimpleHTTPServer
from textwrap import dedent
from cStringIO import StringIO


class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	retries = 0

	def send_head(self):
		if self.path == '/':
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			return StringIO(dedent("""
				Just HTML here.
				<script src="index.js" type="text/javascript"></script>\
			"""))
		elif self.path == '/index.js':
			self.send_response(200)
			self.send_header("Content-type", "application/javascript")
			self.end_headers()
			if self.retries == 0:
				print 'SENDING RST'
				self.retries = 1
				# Send an RST packet.
				nolinger(self.connection)
				self.connection.close()
				return
			else:
				print 'SENDING ACTUAL JS'
				self.retries = 0
				return StringIO(dedent("""
					text = document.createTextNode('Javascript was here!');
					body = document.getElementsByTagName('body')[0];
					body.replaceChild(text, body.firstChild);
				"""))
		elif self.path == '/favicon.ico':
			self.send_response(404)
			self.end_headers()
		else:
			raise ValueError("Unhandled path: %s" % self.path)

def nolinger(s):
	import socket, struct
	l_onoff = 1
	l_linger = 0
	s.setsockopt(
		socket.SOL_SOCKET, socket.SO_LINGER,
		struct.pack('ii', l_onoff, l_linger)
	)

def client(host, port):
	import socket, errno
	BUFFER_SIZE = 2**10
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	nolinger(s)

	s.bind((host, port))
	print 'Listening on %s:%s' % (host, port)
	s.listen(1)
	conn, addr = s.accept()

	print 'Connection address:', addr
	while 1:
		print 'reading...'
		try:
			data = conn.recv(BUFFER_SIZE, socket.MSG_DONTWAIT)
		except Exception, e:
			if e.errno == errno.EWOULDBLOCK:
				break
			else:
				raise

		if not data: break
		print "received data:", data
		conn.send(data)  # echo
	conn.close()

def main0():
	client('0.0.0.0', 8080)

def main():
	import BaseHTTPServer
	httpd = BaseHTTPServer.HTTPServer(('', 8080), MyRequestHandler)
	sa = httpd.socket.getsockname()
	print "Serving HTTP on", sa[0], "port", sa[1], "..."
	httpd.serve_forever()

if __name__ == '__main__':
	main()
