#!/usr/bin/env python
# pylint: disable=I0011,C0111,C0103,W0142
from math import sqrt, copysign

# stdtr( k, t )
# Computes the integral from minus infinity to t of the Student
# t distribution with integer k > 0 degrees of freedom
from scipy.special import stdtr

def sample_variance(sample, mean, n):
    return sum((x - mean)**2 for x in sample) / (n - 1)


def t_statistic(sample, expected_mean):
    n = len(sample)
    mean = float(sum(sample))/n
    s = sample_variance(sample, mean, n)
    if s == 0:
        return copysign(float('inf'), mean - expected_mean)
    else:
        return (mean - expected_mean) / (s / sqrt(n))


def ttest_range(sample, left, right):
    k = len(sample) - 1
    left = stdtr(k, -t_statistic(sample, left))
    print 'left:', left
    right = stdtr(k, t_statistic(sample, right))
    print 'right:', right
    outside = left + right
    print 'outside:', outside
    inside = 1 - outside
    print 'inside:', inside
    return inside

def system():
    import random
    while True:
        yield random.normalvariate(5, 3)
system = system()

satisfactory_range = (4, 6)
required_certainty = .90

def test():
    print 'SATISFACTORY RANGE:', satisfactory_range
    samples = [next(system)]
    print 'SAMPLE:', samples[-1]
    while True:
        samples.append(next(system))
        print 'SAMPLE:', samples[-1]
        probability_inside = ttest_range(samples, *satisfactory_range)
        if probability_inside >= required_certainty:
            return 'PASS (%i samples)' % len(samples)
        elif 1 - probability_inside >= required_certainty:
            return 'FAIL (%i samples)' % len(samples)

if __name__ == '__main__':
    exit(test())
