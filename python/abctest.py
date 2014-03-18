from abc import ABCMeta, abstractproperty, abstractmethod


class IC(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def f(self):
        return 'f'

    @abstractproperty
    def wat(self):
        pass

class C(IC, object):
    wat = 'wat'

    def f(self): pass


print C().wat
