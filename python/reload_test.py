# pylint:disable=missing-docstring,exec-used
import gc
import sys
from textwrap import dedent


class DisableModuleCache(object):
    """Defines a context in which the contents of sys.modules is held constant.
    i.e. Any new entries in the module cache (sys.modules) are cleared when exiting this context.
    """
    modules_before = None
    def __enter__(self):
        self.modules_before = sys.modules.keys()
    def __exit__(self, *args):
        for module in sys.modules.keys():
            if module not in self.modules_before:
                del sys.modules[module]
        gc.collect()  # force collection after removing refs, for demo purposes.


def reload_config(filename):
    """Reload configuration from a file"""
    with DisableModuleCache():
        namespace = {}
        exec open(filename) in namespace
        config = namespace['config']
        del namespace

    config()


def main():
    open('config_module.py', 'w').write(dedent('''
    GLOBAL = 'GLOBAL'
    def config():
        print 'config! (old implementation)'
        print GLOBAL
    '''))

    # if I exec that file itself, its functions maintain a reference to its modules,
    # keeping GLOBAL's refcount above zero
    reload_config('config_module.py')
    ## output:
    #config! (old implementation)
    #GLOBAL

    # If that file is once-removed from the exec, the functions no longer maintain a reference to their module.
    # The GLOBAL's refcount goes to zero, and we get a None value (feels like weakref behavior?).
    open('main.py', 'w').write(dedent('''
    from config_module import *
    '''))

    reload_config('main.py')
    ## output:
    #config! (old implementation)
    #None

    ## *desired* output:
    #config! (old implementation)
    #GLOBAL

    acceptance_test()


def acceptance_test():
    # Have to wait at least one second between edits (on ext3),
    # or else we import the old version from the .pyc file.
    from time import sleep
    sleep(1)

    open('config_module.py', 'w').write(dedent('''
    GLOBAL2 = 'GLOBAL2'
    def config():
        print 'config2! (new implementation)'
        print GLOBAL2

        ## There should be no such thing as GLOBAL. Naive reload() gets this wrong.
        try:
            print GLOBAL
        except NameError:
            print 'got the expected NameError :)'
        else:
            raise AssertionError('expected a NameError!')
    '''))

    reload_config('main.py')
    ## output:
    #config2! (new implementation)
    #None
    #got the expected NameError :)

    ## *desired* output:
    #config2! (new implementation)
    #GLOBAL2
    #got the expected NameError :)



if __name__ == '__main__':
    main()
