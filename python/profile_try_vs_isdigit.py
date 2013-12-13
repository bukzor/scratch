


def try_numbers(inputs):
	result = []
	for i in inputs:
		try:
			result.append(int(i))
		except ValueError:
			result.append(i)
	return result

def if_isdigit_numbers(inputs):
	result = []
	for i in inputs:
		if i.isdigit():
			result.append(int(i))
		else:
			result.append(i)
	return result
	

def generate_fake_inputs(count, numbers_ratio=.5):
	"""
	>>> generate_fake_inputs(3)
	['ecfehde', 'fchgcjjij', '8641469']
	>>> generate_fake_inputs(3, numbers_ratio=1)
	['4254734', '527629989', '8641469']
	>>> generate_fake_inputs(3, numbers_ratio=0)
	['ecfehde', 'fchgcjjij', 'igebegj']
	"""
	from random import seed, random, randrange
	from string import ascii_letters, digits
	seed(0) # repeatable pseudo-random results.
	result = []
	for _ in xrange(count):
		if random() < numbers_ratio:
			characters = digits
		else:
			characters = ascii_letters

		input = ''
		length = randrange(1, 10)
		for _ in xrange(length):
			input += characters[randrange(10)]
		result.append(input)
	return result


def time_them(input, functions):
	from time import time
	results = {}
	previous_output = None
	for function in functions:
		start = time()
		output = function(input)
		end = time()
		results[function] = end - start

		# all functions should have the same output
		if previous_output is not None:
			assert output == previous_output
		previous_output = output
	return results


def main():
	functions = (
			try_numbers,
			if_isdigit_numbers,
	)
	fake_inputs = generate_fake_inputs(100000, numbers_ratio=.9775)

	for _ in xrange(3):
		results = time_them(fake_inputs, functions)
		results = sorted(results.items(), key=lambda item: item[0].__name__)
		previous_time = None
		for function, time in results:
			print '%s: %g' % (function.__name__, time)
			if previous_time is None:
				previous_time = time
			else:
				print 'difference: %.2f%%' % ( (time - previous_time) / previous_time )
		print


if __name__ == '__main__':
	main()
