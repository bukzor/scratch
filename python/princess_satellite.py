#!/usr/bin/env python
'''x'''
GOOGLE = 'http://www.google.com/'

def show_response(resp):
    "x"
    from buck.pprint import pformat as p
    info = resp.info()
    headers = set(h.strip() for h in info.headers)
    cookies = set(h for h in headers if h.startswith('Set-Cookie: '))
    #headers = sorted(headers - cookies)
    cookies = sorted(c[12:] for c in cookies)
    url = resp.geturl()
    

    print 'URL:', resp.geturl()
    print 'STATUS:', resp.getcode()
    import urlparse
    print 'PARAMS:', p(
        urlparse.parse_qsl(urlparse.urlsplit(url).query)
    )
    print 'HEADERS:', p(sorted(headers))
    print 'COOKIES:', p(sorted(cookies))
    print

def main():
    "x"
    from urllib2 import (
            build_opener,
            HTTPCookieProcessor,
    )
    from urllib import urlencode
    opener = build_opener(HTTPCookieProcessor)
    resp = opener.open(GOOGLE)
    show_response(resp)
    if resp.geturl() == GOOGLE:
        return 'already connected!'

    resp = opener.open(
            'http://icsloginweb.icservices.mtnsat.com/LoginV4.aspx',
            urlencode((
                ('PMSv41$txtFirstNameRU', 'Buck'),
                ('PMSv41$txtLastNameRU', 'Golemon'),
                ('PMSv41$txtCabinNumberRU', 'b234'),
                ('PMSv41$txtPasswordRU', 'asdfpasdf'),
                ('__EVENTTARGET', '1'),
                ('__EVENTARGUMENT', ''),
                ('__VIEWSTATE',
                    open('princess_satellite_viewstate.txt').read()
                ),
                ('__VIEWSTATEENCRYPTED', ''),
            )),
    )
    show_response(resp)


if __name__ == '__main__':
    exit(main())
