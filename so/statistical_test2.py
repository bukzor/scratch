from math import ln


def K(p, n, g):
	"""
		p - the desired percentile expressed in the range (0, 1).
		n - the number of samples.
		g - the inverse confidence (1-g is the confidence).
		return -- K - The noncentral t-distribution scaling factor.
	"""
	# Based on equation (2) of:
	# http://128.104.77.228/documnts/fplrp/fplrp458.pdf
	# Link, C. An Equation for One-Sided Tolerance Limits for Normal Distributions. 1985.

	def z_sub_p():
		# equation (3)
		# Also:
		#	http://people.math.sfu.ca/~cbm/aands/page_933.htm
		#	Abramowitz and Stegun (1972, equation 26.2.23):
		t = (ln(1/p**2))**(.5)
		c0 = 2.515517
		c1 = 0.802853
		c2 = 0.010328
		d1 = 1.432788
		d2 = 0.189269
		d3 = 0.001308

		return t - (c0 + c1 * t + c2 * t**2) / (1 + d1 * t + d2 * t ** 2 + d3 * t ** 3)

	zp = z_sub_p()
	f = 1/(4*(n - 1))


	# split up the numerator / denominator of the equation, just for readability.
	K_numer = zp * (1 - f) + (zp ** 2 * (1 - f) ** 2 - ((1-f)**2 - zg**2/(2*(n - 1))) * (zp - zg**2/n)) ** (.5)
	K_denom = (1 - f)**2 - zg**2 / (2*(n - 1))
	
	return K_numer / K_denom
