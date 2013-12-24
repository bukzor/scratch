# I0011: disabling locally
# C0111: missing docstring
# W0122: use of exec
# pylint:disable=I0011,C0111,W0122
def main():
    open('sub.py', 'w').write('''
    def foo():
            print 'foo!'
    def bar():
            print 'bar!'
    ''')

    open('main.py', 'w').write('''
    import sys

    # Three possibile strategies for getting a fresh import.
    def strat4():
            del sys.modules['sub']

    from sub import foo
    foo()

    from sub import bar
    bar()

    strat4()
    ''')

    namespace = {}
    exec open('main.py') in namespace

    # Have to wait at least one second between edits,
    # or else we import the old version from the .pyc file.
    from time import sleep
    sleep(1)

    open('sub.py', 'w').write('''
    def foo():
            print 'foo: bar!'
    ''')

    namespace = {}
    try:
        exec open('main.py') in namespace
        error = None
    except ImportError, error:
        pass
    assert error

    import sys
    print sys.modules.pop('sub')


if __name__ == '__main__':
    main()
