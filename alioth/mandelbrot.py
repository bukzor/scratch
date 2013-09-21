#!/usr/bin/env python3
# pylint:disable=I0011,C0111,W0622,C0103,W0142,W0511,R0914

def main(N=100):
    N = int(N)
    buf = []

    M = 2.0/N
    ba = 2**(N%8+1)-1
    bb = 2**(8-N%8)

    for y in range(N):
        Ci = y*M-1
        b = 1
        for x in range(N):
            Cr = x*M-1.5
            Zr = Cr
            Zi = Ci
            Zrq = Cr**2
            Ziq = Ci**2
            b = b + b # TODO left shift
            for _ in range(1, 50):
                Zi = Zr*Zi*2 + Ci # TODO left shift
                Zr = Zrq - Ziq + Cr
                Ziq = Zi**2 # TODO test versus multiply
                Zrq = Zr**2
                if Zrq + Ziq > 4.0:
                    b = b + 1 # TODO test versus += 1
                    break
            if b >= 256: # TODO test versus float compare
                buf.append(511 - b)
                b = 1
        if b != 1:
            buf.append((ba - b) * bb)

    # See mandelbrot.benchmarks/io.py
    stdout = open('/dev/stdout', 'wb')
    stdout.write(("P4\n%i %i\n" % (N, N)).encode('ascii'))
    stdout.write(bytes(buf))


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
