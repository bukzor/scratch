# -*- coding: UTF-8 -*-
def recode_utf8(data):
	"""
	Given a string which is either:
	 * unicode
	 * well-encoded utf8
	 * well-encoded latin1
	 * poorly-encoded utf8+latin1
	Return the equivalent utf8-encoded byte string.
	"""
	if isinstance(data, unicode):
		# The input is already decoded. Just return the utf8.
		return data.encode('UTF-8')

	try:
		decoded = data.decode('UTF-8')
	except UnicodeDecodeError:
		# Indicates latin1 encoded bytes.
		decoded = data.decode('latin1')

	while True:
		# Check if the data is poorly-encoded as utf8+latin1
		try:
			encoded = decoded.encode('latin1')
		except UnicodeEncodeError:
			# Indicates non-latin1-encodable characters; it's not utf8+latin1.
			return decoded.encode('UTF-8')

		try:
			decoded = encoded.decode('UTF-8')
		except UnicodeDecodeError:
			# Can't decode the latin1 as utf8; it's not utf8+latin1.
			return decoded.encode('UTF-8')


import unittest as T
class TestRecodeUtf8(T.TestCase):
	latin1 = u'München' # encodable to latin1
	utf8 = u'Łódź' # not encodable to latin1

	def test_unicode(self):
		"An un-encoded unicode string should just become utf8-encoded"
		self.assertEqual(
				recode_utf8(self.utf8),
				self.utf8.encode('UTF-8'),
		)

	def test_utf8(self):
		"A utf8-encoded string should be unchanged"
		utf8 = self.utf8.encode('UTF-8')
		self.assertEqual(
				recode_utf8(utf8),
				utf8,
		)

	def test_latin1(self):
		"A latin1-encoded string should become utf8-encoded"
		self.assertEqual(
				recode_utf8(self.latin1.encode('latin1')),
				self.latin1.encode('UTF-8'),
		)

	def test_utf8_plus_latin1(self):
		"A poorly-encoded utf8+latin1 string should become utf8-encoded"
		utf8 = self.utf8.encode('UTF-8')
		poorly_encoded = utf8.decode('latin1').encode('UTF-8')
		self.assertEqual(
				recode_utf8(poorly_encoded),
				utf8,
		)

	def test_utf8_plus_latin1_several_times(self):
		"A string mangled by utf8+latin1 several times should become utf8-encoded"
		utf8 = self.utf8.encode('UTF-8')
		poorly_encoded = utf8
		for x in range(10):
			poorly_encoded = poorly_encoded.decode('latin1').encode('UTF-8')

		self.assertEqual(
				recode_utf8(poorly_encoded),
				utf8,
		)



if __name__ == '__main__':
	T.main()
