# pylint:disable=blacklisted-name,missing-docstring,invalid-name,multiple-statements,bad-whitespace,too-many-public-methods
fset = frozenset

class token(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Not(object):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return 'Not(%r)' % self.obj

    def __eq__(self, other):
        if isinstance(other, Not):
            return self.obj == other.obj
        else:
            return NotImplemented

    def __hash__(self):
        return hash((Not, self.obj))


def notter(setlist, obj):
    result = []
    for s in setlist:
        if obj in s:
            result.append(s)
        else:
            result.append(s | fset([Not(obj)]))
    return result


def solve(setlist):
    allstates = reduce(fset.union, setlist)
    #for state in tuple(allstates):
        #if not isinstance(state, Not):
            #allstates |= fset([Not(state)])
    print 'all states:', allstates

    stack = [(setlist, allstates, fset())]
    while stack:
        setlist, unsolved, solved = stack.pop()
        print 'POP:', setlist, unsolved, solved
        if allstates == solved:
            yield setlist
            continue

        from collections import defaultdict
        count = defaultdict(int)
        for state in unsolved:
            for s in setlist:
                if state in s:
                    count[state] += 1
        count = sorted((val, key) for key, val in count.items())
        for c in count:
            print c

        state = count[0][1]
        print 'solving:', state

        has = set()
        for s in setlist:
            if state in s:
                has.add(s)

        tmp = []
        for s in setlist:
            if s in has:
                tmp.append(s)
            elif any(AND(s, h) for h in has):
                tmp.append(s | fset([Not(state)]))
            else:
                tmp.append(s)
        setlist = tmp

        unsolved -= fset([state])
        solved |= fset([state])
        stack.append((setlist, unsolved, solved))
        print


A = token('A')
B = token('B')
C = token('C')
D = token('D')
E = token('E')


def AND(s1, s2):
    if any(Not(x) in s2 for x in s1):
        return fset()

    if any(Not(x) in s1 for x in s2):
        return fset()

    return s1 | s2



from unittest import TestCase
class MyTest(TestCase):
    def assert_solved(self, input, answer):  # pylint:disable=redefined-builtin
        result = tuple(solve(input))[0]
        from pprint import pprint
        pprint(result)
        pprint(answer)
        self.assertEqual(result, answer)

    def test_simple(self):
        self.assert_solved(
            [
                fset([]),
                fset([B]),
            ],
            [
                fset([Not(B)]),
                fset([B]),
            ],
        )

    def test_two(self):
        self.assert_solved(
            [
                fset([]),
                fset([A]),
                fset([B]),
            ],
            [
                fset([Not(A), Not(B)]),
                fset([A]),
                fset([B, Not(A)]),
            ],
        )

    def test_two2(self):
        self.assert_solved(
            [
                fset([]),
                fset([A]),
                fset([A, B]),
            ],
            [
                fset([Not(A)]),
                fset([A, Not(B)]),
                fset([A, B]),
            ],
        )

    def test_three(self):
        self.assert_solved(
            [
                fset([]),
                fset([A]),
                fset([A, B]),
                fset([C])
            ],
            [
                fset([Not(A), Not(C)]),
                fset([A, Not(B), Not(C)]),
                fset([A, B, Not(C)]),
                fset([C])
            ],
        )


    def XXtest_first(self):
        self.assert_solved(
            [
                fset([]),
                fset([B]),
                fset([C]),
                fset([B, C]),
                fset([D]),
                fset([E]),
                fset([B, E]),
            ],
            [  # flake8:noqa
                fset([Not(B), Not(C), Not(D), Not(E)]),
                fset([    B,  Not(C), Not(D), Not(E)]),
                fset([Not(B),     C,  Not(D), Not(E)]),
                fset([    B,      C,  Not(D), Not(E)]),
                fset([                    D]),
                fset([Not(B),                     E]),
                fset([    B,                      E]),
            ],
        )

class TestAND(TestCase):
    def test_simplest(self):
        self.assertEqual(
            AND(fset(), fset()),
            fset(),
        )

    def test_one(self):
        self.assertEqual(
            AND(fset([A]), fset()),
            fset([A]),
        )

    def test_two(self):
        self.assertEqual(
            AND(fset([A, B]), fset()),
            fset([A, B]),
        )

    def test_two2(self):
        self.assertEqual(
            AND(fset([A]), fset([B])),
            fset([A, B]),
        )

    def test_Not(self):
        self.assertEqual(
            AND(fset([A]), fset([Not(B)])),
            fset([A, Not(B)]),
        )

    def test_Not2(self):
        self.assertEqual(
            AND(fset([A]), fset([Not(A)])),
            fset(),
        )

    def test_Not3(self):
        self.assertEqual(
            AND(fset([A, B]), fset([Not(A), C])),
            fset(),
        )

def OR(s1, s2):
    return s1 & s2

class TestOR(TestCase):
    def test_simplest(self):
        self.assertEqual(
            OR(fset(), fset()),
            fset(),
        )

    def test_one(self):
        self.assertEqual(
            OR(fset([A]), fset()),
            fset(),
        )

    def test_one2(self):
        self.assertEqual(
            OR(fset([A]), fset([A])),
            fset(fset([A])),
        )

    def test_two(self):
        self.assertEqual(
            OR(fset([A, B]), fset()),
            fset(),
        )

    def test_two2(self):
        self.assertEqual(
            OR(fset([A]), fset([B])),
            fset(fset([A]), fset([B])),
        )

    def test_Not(self):
        self.assertEqual(
            OR(fset([A]), fset([Not(B)])),
            fset([A, Not(B)]),
        )

    def test_Not2(self):
        self.assertEqual(
            OR(fset([A]), fset([Not(A)])),
            fset(),
        )

    def test_Not3(self):
        self.assertEqual(
            OR(fset([A, B]), fset([A, Not(B)])),
            fset([fset([A])]),
        )


if __name__ == '__main__':
    from unittest import main
    exit(main())
