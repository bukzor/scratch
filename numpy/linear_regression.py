# pylint:disable=missing-docstring,g-import-not-at-top
import numpy

np = numpy


def np_cols(*columns):
  return np.column_stack(columns)


def np_rows(*rows):
  return np.row_stack(rows)


def total_error(actual, expected):
  return np.sum(abs(actual - expected))


x = np.array([1, 2, 4, 5, 6, 7, 8, 9, 10, 3, 20])
x2 = np.array([x]).T
m1 = 0.1
b1 = 2
y1 = m1 * x + b1
m2 = b2 = -1
y2 = m2 * x + b2
m3 = 3
b3 = 7
y3 = m3 * x + b3

print(" x:", x)
print("y1:", y1)
print("y2:", y2)
print("y3:", y3)

m = np.array([m1, m2, m3])
b = np.array([b1, b2, b3])
print(" m:", m)
print(" b:", b)


y = np_cols(y1, y2, y3)
print(" y:")
print(y)

print("m*x + b:")
print(m * np_cols(x) + b)

print("y == m*x + b")
assert (y == m * np_cols(x) + b).all()

x1 = np_cols(x, np.ones(x.shape))
print("x1:")
print(x1)
mb = np_rows(m, b)
print("mb:")
print(mb)

print("y == x1 · mb")
assert (y == np.dot(x1, mb)).all()


def pad_to_square(a):
  a = a.reshape((a.shape[0], -1))
  size = max(a.shape)
  padded = np.identity(size)
  padded[0 : a.shape[0], 0 : a.shape[1]] = a
  return padded


def entallen(a, height):
  return np.pad(a, ((0, height - a.shape[0]), (0, 0)))


x1_square = pad_to_square(x1)
print("x1_square:")
print(x1_square)

mb_tall = entallen(mb, x1_square.shape[1])
print("mb_tall:")
print(mb_tall)

print("y == x1_square · mb_tall")
assert (y == np.dot(x1_square, mb_tall)).all()


print()
print("solutions:")
print("=" * 40)


def assert_solution(label, actual, expected):
  error = total_error(actual, expected)
  print(f"{label:<18} error: {error:<11g}")
  assert numpy.allclose(actual, expected)


solution1 = np.linalg.solve(x1_square, y)
assert_solution("numpy.linalg.solve", solution1, mb_tall)

solution2, residues, rank, s = numpy.linalg.lstsq(x1, y, rcond=None)
assert_solution("numpy.linalg.lstsq", solution2, mb)

solution30 = numpy.polyfit(x, y, 1)
assert_solution("numpy.polyfit", solution30, mb)

import scipy.linalg

solution3 = scipy.linalg.solve(x1_square, y)
assert_solution("scipy.linalg.solve", solution3, mb_tall)

solution4, residues, rank, s = scipy.linalg.lstsq(x1, y)
assert_solution("scipy.linalg.lstsq", solution4, mb)

x1inv = np.dot(np.linalg.inv(np.dot(x1.T, x1)), x1.T)
solution5 = np.dot(x1inv, y)
assert_solution("np.linalg.inv", solution5, mb)

x1inv = np.linalg.pinv(x1)
solution5 = np.dot(x1inv, y)
assert_solution("np.linalg.pinv", solution5, mb)
