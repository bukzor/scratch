import sys
def myexcepthook(exctype, value, traceback):
    if exctype == SyntaxError and value.text == 'say what':
        from os import system
        system('exec toilet -tf bigmono9 --gay %s indeed.' % value.text)
    else:
        sys.__excepthook__(exctype, value, traceback)
sys.excepthook = myexcepthook


eval('say what')
