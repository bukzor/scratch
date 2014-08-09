#!/usr/bin/env python

from errno import EEXIST
from os import mkdir, curdir
from os.path import split, exists

def mkdirp(path, mode=0777):
    head, tail = split(path)
    if not tail:
        head, tail = split(head)
    if head and tail and not exists(head):
        try:
            mkdirp(head, mode)
        except OSError, e:
            # be happy if someone already created the path
            if e.errno != EEXIST:
                raise
        if tail == curdir:  # xxx/newdir/. exists if xxx/newdir exists
            return
    try:
        mkdir(path, mode)
    except OSError, e:
        # be happy if someone already created the path
        if e.errno != EEXIST:
            raise



def main():
    from sys import argv
    for path in argv[1:]:
        mkdirp(path)


if __name__ == '__main__':
    exit(main())
