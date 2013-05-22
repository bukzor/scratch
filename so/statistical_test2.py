#!/usr/bin/env python
from math import log as ln


def K(p, g, n):
	"""
		p - the desired percentile expressed in the range (0, 1).
		g - the inverse confidence (1-g is the confidence).
		n - the number of samples.
		return -- K - The noncentral t-distribution scaling factor.
	"""
	# Based on equation (2) of:
	# http://128.104.77.228/documnts/fplrp/fplrp458.pdf
	# Link, C. An Equation for One-Sided Tolerance Limits for Normal Distributions. 1985.
	p = float(p)
	g = float(g)
	n = float(n)

	def z(x):
		# equation (3)
		# Also:
		#	http://people.math.sfu.ca/~cbm/aands/page_933.htm
		#	Abramowitz and Stegun (1972, equation 26.2.23):
		t = (ln(1/x**2))**(.5)
		c0 = 2.515517
		c1 = 0.802853
		c2 = 0.010328
		d1 = 1.432788
		d2 = 0.189269
		d3 = 0.001308

		return t - (c0 + c1 * t + c2 * t**2) / (1 + d1 * t + d2 * t**2 + d3 * t**3)

	zp = z(p)
	zg = z(g)
	f = 1/(4*(n - 1))

	# split up the numerator / denominator of the equation, just for readability.
	K_numer = zp * (1 - f) + (zp**2 * (1 - f)**2 - ((1-f)**2 - zg**2/(2*(n - 1))) * (zp**2 - zg**2/n))**(.5)
	K_denom = (1 - f)**2 - zg**2 / (2*(n - 1))
	
	return K_numer / K_denom

def main():
	for p, g, n, lieberman, equation_2, Guttman in (
			(.1, .25, 10, 1.6154, 1.6683, 1.671),
			(.05, .05, 50, 2.0590, 2.0713, 2.065),
			(.01, .05, 200, 2.5684, 2.5719, 2.570),
	):
		print '\t'.join(
				'% -8g' % x for x in (p, g, n, lieberman, equation_2, Guttman, K(p, g, n))
		)


if __name__ == '__main__':
	main()
