# encoding:UTF-8

from MySQLdb import connect

# TODO: resolve the ~
conn = connect(user='root', unix_socket='~/tmp/mysql/mysql.sock', charset='utf8')

#conn.set_character_set('utf8')

cursor = conn.cursor()
cursor.execute('select %s', u"Łódź")
for row in cursor:
	print row[0]
