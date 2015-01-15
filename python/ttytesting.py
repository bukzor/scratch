from __future__ import print_function
import os
import termios

read, write = os.openpty()
os.write(write, 'hi there!\n')
output = os.read(read, 1024)
expected = 'hi there!\r\n'
assert output == expected, repr(output)


def fix_pty_newlines(fd):
    r"""
    Twiddle the tty flags such that \n won't get munged to \r\n.
    Details:
        https://docs.python.org/2/library/termios.html
        http://ftp.gnu.org/old-gnu/Manuals/glibc-2.2.3/html_chapter/libc_17.html#SEC362
    """
    attrs = termios.tcgetattr(fd)
    attrs[1] &= ~(termios.ONLCR | termios.OPOST)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)


fix_pty_newlines(read)

os.write(write, 'hi there!\n')
output = os.read(read, 1024)
expected = 'hi there!\n'
assert output == expected, repr(output)


flags = {
    'iflag': (
        'IGNBREAK', 'BRKINT', 'IGNPAR', 'PARMRK', 'INPCK', 'ISTRIP', 'INLCR', 'IGNCR', 'ICRNL', 'IXON', 'IXOFF',
        'IXANY', 'IMAXBEL', 'IUCLC',
    ),
    'oflag': ('OPOST', 'ONLCR', 'OXTABS', 'ONOEOT', 'OCRNL', 'OLCUC', 'ONOCR', 'ONLRET'),
    'cflag': (
        'CSIZE', 'CS5', 'CS6', 'CS7', 'CS8', 'CSTOPB', 'CREAD', 'PARENB', 'PARODD', 'HUPCL', 'CLOCAL', 'CCTS_OFLOW',
        'CRTSCTS', 'CRTS_IFLOW', 'MDMBUF', 'CIGNORE',
    ),
    'lflag': (
        'ECHOKE', 'ECHOE', 'ECHO', 'ECHONL', 'ECHOPRT', 'ECHOCTL', 'ISIG', 'ICANON', 'ALTWERASE', 'IEXTEN', 'EXTPROC',
        'TOSTOP', 'FLUSHO', 'NOKERNINFO', 'PENDIN', 'NOFLSH', 'ECHOK',
    ),
    'ispeed': (
        'B0', 'B50', 'B75', 'B110', 'B134', 'B150', 'B200', 'B300', 'B600', 'B1200', 'B1800', 'B2400', 'B4800', 'B9600',
        'B19200', 'B38400', 'B57600', 'B115200', 'B230400', 'B460800',
    ),
    'cc': (
        'CEOF', 'CEOL', 'CEOT', 'CERASE', 'CWERASE', 'CKILL', 'CRPRNT', 'CINTR', 'CQUIT', 'CSUSP', 'CDSUSP',
        'CSTART', 'CSTOP', 'CLNEXT', 'CDISCARD', 'CMIN', 'CTIME', 'CSTATUS',
    ),
}
flags['ospeed'] = flags['ispeed']


def termios_flags():
    termios.CDISCARD = 0x0F
    termios.CMIN = 0x01
    termios.CTIME = 0x00
    termios.CSTATUS = 0x14
    return dict(
        (attr, value)
        for attr, value in vars(termios).items()
        if isinstance(value, int)
    )
termios_flags = termios_flags()


def show_bitflags(attr, val):
    notfound = val
    for flag in sorted(flags[attr]):
        if flag not in termios_flags:
            continue
        flagval = termios_flags[flag]
        if val & flagval == flagval:
            print('       ', flag, flagval)
            notfound &= ~flagval
    return notfound


def show_charlist(attr, val):
    notfound = list(val)
    for i, part in enumerate(val):
        for flag in sorted(flags[attr]):
            if flag not in termios_flags:
                continue
            flagval = termios_flags[flag]
            flagval = chr(flagval)
            if part == flagval:
                print('       ', i, flag, repr(flagval))
                if flagval in notfound:
                    notfound.remove(flagval)
    return notfound


def main():
    for name, fd in (
            ('read pipe:', read),
            ('write pipe:', write),
    ):
        print(name)
        for attr, val in zip(
                ('iflag', 'oflag', 'cflag', 'lflag', 'ispeed', 'ospeed', 'cc'),
                termios.tcgetattr(fd),
        ):
            print('   ', attr, val)
            if isinstance(val, int):
                notfound = show_bitflags(attr, val)
            else:
                notfound = show_charlist(attr, val)
            if notfound:
                print('FLAGS NOT FOUND:', attr, notfound)


if __name__ == '__main__':
    exit(main())

output = '''\
read pipe:
    iflag 11010
        BRKINT 2
        ICRNL 256
        IMAXBEL 8192
        IXANY 2048
        IXON 512
    oflag 3
        ONLCR 2
        OPOST 1
    cflag 19200
        CREAD 2048
        CS5 0
        CS6 256
        CS7 512
        CS8 768
        CSIZE 768
        HUPCL 16384
    lflag 1483
        ECHO 8
        ECHOCTL 64
        ECHOE 2
        ECHOKE 1
        ICANON 256
        IEXTEN 1024
        ISIG 128
    ispeed 9600
        B0 0
        B9600 9600
    ospeed 9600
        B0 0
        B9600 9600
    cc ['\x04', '\xff', '\xff', '\x7f', '\x17', '\x15', '\x12', '\xff', '\x03', '\x1c', '\x1a', '\x19', '\x11', '\x13', '\x16',
    '\x0f', '\x01', '\x00', '\x14', '\xff']
        0 CEOF '\x04'
        0 CEOT '\x04'
        1 CEOL '\xff'
        2 CEOL '\xff'
        3 CERASE '\x7f'
        4 CWERASE '\x17'
        5 CKILL '\x15'
        6 CRPRNT '\x12'
        7 CEOL '\xff'
        8 CINTR '\x03'
        9 CQUIT '\x1c'
        10 CSUSP '\x1a'
        11 CDSUSP '\x19'
        12 CSTART '\x11'
        13 CSTOP '\x13'
        14 CLNEXT '\x16'
        15 CDISCARD '\x0f'
        16 CMIN '\x01'
        17 CTIME '\x00'
        18 CSTATUS '\x14'
        19 CEOL '\xff'
write pipe:
    iflag 11010
        BRKINT 2
        ICRNL 256
        IMAXBEL 8192
        IXANY 2048
        IXON 512
    oflag 3
        ONLCR 2
        OPOST 1
    cflag 19200
        CREAD 2048
        CS5 0
        CS6 256
        CS7 512
        CS8 768
        CSIZE 768
        HUPCL 16384
    lflag 1483
        ECHO 8
        ECHOCTL 64
        ECHOE 2
        ECHOKE 1
        ICANON 256
        IEXTEN 1024
        ISIG 128
    ispeed 9600
        B0 0
        B9600 9600
    ospeed 9600
        B0 0
        B9600 9600
    cc ['\x04', '\xff', '\xff', '\x7f', '\x17', '\x15', '\x12', '\xff', '\x03', '\x1c', '\x1a', '\x19', '\x11', '\x13', '\x16',
    '\x0f', '\x01', '\x00', '\x14', '\xff']
        0 CEOF '\x04'
        0 CEOT '\x04'
        1 CEOL '\xff'
        2 CEOL '\xff'
        3 CERASE '\x7f'
        4 CWERASE '\x17'
        5 CKILL '\x15'
        6 CRPRNT '\x12'
        7 CEOL '\xff'
        8 CINTR '\x03'
        9 CQUIT '\x1c'
        10 CSUSP '\x1a'
        11 CDSUSP '\x19'
        12 CSTART '\x11'
        13 CSTOP '\x13'
        14 CLNEXT '\x16'
        15 CDISCARD '\x0f'
        16 CMIN '\x01'
        17 CTIME '\x00'
        18 CSTATUS '\x14'
        19 CEOL '\xff'
'''
