
from functools import wraps
from time import sleep

def dec1(func):
	@wraps(func)
	def wrapper():
		sleep(.1)
		return func()
	return wrapper

@dec1
def func1():
	sleep(.5)

@dec1
def func2():
	sleep(1)

def main():
	sleep(.1)
	func1()
	func2()



if __name__ == '__main__':
	main()
