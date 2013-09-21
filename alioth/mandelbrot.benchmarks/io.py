#!/usr/bin/env python3
# msgfrag.py
#
# Demonstrate performance of different python3 io strategies.

from timethis import timethis

FRAGMENT_SIZE = 256
NUMBER_FRAGS  = 10000

# A generator that creates byte fragments for us
def make_fragments(size,count):
    frag = b"x"*size
    while count > 0:
        yield frag
        count -= 1

def test():
    ## This is super slow.
    # Try byte concatenation
    #with timethis("Byte concatenation +="):
        #msg = b""
        #for chunk in make_fragments(FRAGMENT_SIZE, NUMBER_FRAGS):
            #msg += chunk

    # Try .join()
    with timethis("Joining a list of fragments"):
        msgparts = []
        for chunk in make_fragments(FRAGMENT_SIZE, NUMBER_FRAGS):
            msgparts.append(chunk)
        msg = b"".join(msgparts)
        open('/dev/null', 'wb').write(msg)

    # Try bytearray.extend
    with timethis("Extending a bytearray"):
        msg = bytearray()
        for chunk in make_fragments(FRAGMENT_SIZE, NUMBER_FRAGS):
            msg.extend(chunk)
        open('/dev/null', 'wb').write(msg)

    with timethis("BytesIO"):
        from io import BytesIO
        msg = BytesIO()
        for chunk in make_fragments(FRAGMENT_SIZE, NUMBER_FRAGS):
            msg.write(chunk)
        open('/dev/null', 'wb').write(msg.read())

    with timethis("FileIO"):
        from io import FileIO
        msg = FileIO('/dev/null', 'w')
        for chunk in make_fragments(FRAGMENT_SIZE, NUMBER_FRAGS):
            msg.write(chunk)

    with timethis("open, wb"):
        msg = open('/dev/null', 'wb')
        for chunk in make_fragments(FRAGMENT_SIZE, NUMBER_FRAGS):
            msg.write(chunk)



for i in range(500):
    test()
