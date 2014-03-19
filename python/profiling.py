# pylint:disable=C0111,C0103
def longsleep():
    sleep(1)

def shortsleep():
    sleep(.1)

def sleep(n):
    import time
    time.sleep(n)

def call(f):
    return f()

def fast_call():
    call(shortsleep)

def slow_call():
    call(longsleep)

def main():
    fast_call()
    slow_call()

if __name__ == '__main__':
    exit(main())
