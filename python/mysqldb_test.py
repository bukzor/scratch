# encoding:UTF-8

def main():
    from MySQLdb import connect

    # TODO: resolve the ~
    conn = connect(user='root', unix_socket='~/tmp/mysql/mysql.sock', charset='utf8')

    #conn.set_character_set('utf8')

    cursor = conn.cursor()
    cursor.execute('select %s', u"Łódź")
    for row in cursor:
            print row[0]

if __name__ == '__main__':
    main()
