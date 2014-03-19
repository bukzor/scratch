



class Base(object):
    def __init__(self):
        print 'initing Base'

class BaseA(Base):
    def __init__(self):
        print 'initing BaseA'
        res = super(BaseA, self).__init__()

class BaseB(BaseA):
    def __init__(self):
        print 'initing BaseB'
        res = super(BaseA, self).__init__()

class BaseC(BaseA):
    def __init__(self):
        print 'initing BaseC'
        res = super(BaseC, self).__init__()

class BaseD(BaseB, BaseC):
    def __init__(self):
        print 'initing BaseD'
        res = super(BaseD, self).__init__()

print BaseD()
