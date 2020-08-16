#!/usr/bin/env python3
"""
Profiling:

    trials=100; seq $trials |
        xargs --replace  timeout -s INT 0.05 python3 -S primes.py 0.1 |
        tee primes.log
    sort -n primes.log > primes.log.sorted; mv primes.log.sorted primes.log
    echo; tail primes.log
    awk '{ print int((($1 / 50000) ^ 1)* 100) }' primes.log |
        braillegraph

profile side-by-side:

     (echo 9; echo 7) |
        xargs --replace echo primes.log.{} |
        xargs cat |
        awk '{ print int((($1 / 50000) ^ 2)* 60) }' |
        braillegraph
"""


def is_prime(candidate, primes):
    """Is it prime?"""
    for prime, prime_squared in primes:
        if prime_squared > candidate:
            return True
        elif candidate % prime == 0:
            return False
    else:
        raise AssertionError("Too few primes passed")


def primes():
    """Generate all primes."""
    candidate = 3
    square = 9
    primes = [(3, 9)]
    #primes = [3]

    yield 2
    yield 3
    while True:
        #square += (candidate << 2) + 4  # .3
        #square += (candidate + 1) << 2  # .2 .8
        #square += (candidate + 1) * 4  # .4
        square += candidate * 4 + 4  # .5 .7
        candidate += 2
        #square = candidate ** 2

        if is_prime(candidate, primes):
            prime = candidate
            yield prime
            primes.append((prime, square))
            #primes.append(prime)


def main():
    try:
        for prime in primes():
            pass
    except KeyboardInterrupt:
        print(prime)


def main1():
    for prime in primes():
        print(prime)
        return


def main0():
    from sys import argv
    larger_than = int(argv[1])
    for prime in primes():
        if prime > larger_than:
            print(prime)
            break


if __name__ == '__main__':
    from sys import exit
    exit(main())
