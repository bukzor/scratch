from __future__ import print_function
from threading import Thread
from time import sleep


def slow_output(char):
    while True:
        print(char)
        sleep(.1)


threads = [
    Thread(target=slow_output, args=(char,))
    for char in '.%|'
]

for t in threads:
    t.daemon=True
    t.start()

sleep(10000)
