from time import sleep

def main():
    try:
        sleep(10000)
    finally:
        print "Caught!"

if __name__ == '__main__':
    main()
