#!/usr/bin/env python
from math import log as ln
from math import sqrt


def x(p):
	# equation (3)
	# Also:
	#	http://people.math.sfu.ca/~cbm/aands/page_933.htm
	#	Abramowitz and Stegun (1972, equation 26.2.23):
	t = sqrt(ln(1/p**2))
	c0 = 2.515517
	c1 = 0.802853
	c2 = 0.010328
	d1 = 1.432788
	d2 = 0.189269
	d3 = 0.001308

	return t - (c0 + c1 * t + c2 * t**2) / (1 + d1 * t + d2 * t**2 + d3 * t**3)

def x_scipy(p):
	import scipy.stats
	q = 1 - p
	return scipy.stats.norm.ppf(q)

def K(p, g, n, x=x):
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


	zp = x(p)
	zg = x(g)
	f = 1/(4*(n - 1))

	# split up the numerator / denominator of the equation, just for readability.
	K_numer = zp * (1 - f) + sqrt(zp**2 * (1 - f)**2 - ((1-f)**2 - zg**2/(2*(n - 1))) * (zp**2 - zg**2/n))
	K_denom = (1 - f)**2 - zg**2 / (2*(n - 1))
	
	return K_numer / K_denom


def K_scipy(p, g, n):
	from scipy.stats import nct
	return nct.ppf(1-g, n-1, sqrt(n) * x_scipy(p)) / sqrt(n)


def g_(p, n, K):
	from scipy.stats import nct
	return 1 - nct.cdf(sqrt(n) * K, n-1, sqrt(n) * x_scipy(p))


def main():
	for p, g, n, lieberman, equation_2, Guttman in (
			(.10, .25,  10, 1.6154, 1.6683, 1.671),
			(.05, .05,  50, 2.0590, 2.0713, 2.065),
			(.01, .05, 200, 2.5684, 2.5719, 2.570),
			(.05, .25,  10, 2.0322, 2.0995, 2.104),
			(.05, .25,  50, 1.8005, 1.8103, 1.811),
			(.05, .25, 100, 1.7529, 1.7575, 1.758),
			(.05, .25, 200, 1.7204, 1.7226, 1.723),
	):
		basis = 0
		print ' '.join(
				'% -12.7g' % x for x in (
					p,
					g,
					(g_(p, n, K_scipy(p, g, n)) - g)/g,
					n,
					lieberman - basis,
					equation_2 - basis,
					Guttman - basis,
					K_scipy(p, g, n) - basis,
					K(p, g, n, x=x_scipy) - basis,
					K(p, g, n) - basis,
				)
		)


if __name__ == '__main__':
	main()
