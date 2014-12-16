"""run as:

yes | xargs --replace sh -c 'rm -rf tmpvenv/ && python stage1.py < /dev/tty'

"""


def shellescape(args):
    from pipes import quote
    return ' '.join(quote(arg) for arg in args)


def colorize(cmd):
    return '\033[01;36m>\033[m \033[01;32m{0}\033[m'.format(shellescape(cmd))


def run(cmd):
    from subprocess import check_call
    check_call(('echo', colorize(cmd)))
    check_call(cmd)


def main():
    venv_path = 'tmpvenv'

    import sys
    run((sys.executable, '-m', 'virtualenv', venv_path))

    from os.path import join
    venv_python = join(venv_path, 'bin', 'python')

    from os import environ
    environ.pop('__PYVENV_LAUNCHER__', None)  # this thing clobbers python's sys.executable
    # It's set by all OSX python executables  t.t

    run((venv_python, 'stage2.py'))


if __name__ == '__main__':
    exit(main())
