import testify.assertions as T
from unittest import TestCase

from frozendict import FrozenDict

class FrozenDictTestCase(TestCase):
    def test_is_immutable(self):
        fd = FrozenDict(a=1)
        T.assert_equal(fd['a'], 1)

        with T.assert_raises(TypeError):
            fd['a'] = 2

    def test_is_immutable2(self):
        # some simple frozendict implementations would mutate here.
        fd = FrozenDict(a=1)
        with T.assert_raises(TypeError):
            dict.update(fd, {'a':2})

    def test_update(self):
        ################################
        # a b c d e f g h i j k l m n o
        # * * * * * * * *
        # * * * *         * * * *
        # * *     * *     * *     * *
        # *   *   *   *   *   *   *   *
        fd = FrozenDict(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8)
        fd2 = fd.update(
                dict(a=9, b=10, c=11, d=12, i=13, j=14, k=15, l=16),
                (
                    (key, val)
                    for key, val in zip(
                        ('a', 'b', 'e', 'f', 'i', 'j', 'm', 'n'),
                        range(17, 25),
                    )
                ),
                a=25, c=26, e=27, g=28, i=29, k=30, m=31, o=32
        )
        expected = dict(
                a=25, b=18, c=26, d=12, e=27, f=20, g=28, h=8,
                i=29, j=22, k=30, l=16, m=31, n=24, o=32,
        )
        assert fd2 == expected

    def test_can_hash(self):
        # Only immutable objects are hashable, and hashable objects can be dict keys.
        fd1 = FrozenDict(a=1, b=2)
        fd2 = FrozenDict({'a':1, 'b':2})

        mydict = {fd1:1}
        mydict[fd2] = 2

        T.assert_equal(mydict[fd1], 2)

    def test_cheap_copy(self):
        fd = FrozenDict()
        T.assert_is(fd, fd.copy())

    def test_no_attributes_allowed(self):
        fd = FrozenDict()
        with T.assert_raises(AttributeError):
            fd.x = 1

    def test_no_attribute_deletion(self):
        fd = FrozenDict()
        with T.assert_raises(AttributeError):
            del fd.copy
    
    def test_cheap_hash(self):
        import mock
        import __builtin__
        with mock.patch.object(__builtin__, 'hash', wraps=hash) as mock_hash:
            fd = FrozenDict(a=1)

            T.assert_equal((('a', 1),).__hash__(), fd.__hash__())
            T.assert_equal(1, mock_hash.call_count)

            T.assert_equal((('a', 1),).__hash__(), fd.__hash__())
            T.assert_equal(1, mock_hash.call_count)
    
    def test_no_vars(self):
        """To allocate a .__dict__ attribute of this object means that we're allocating a second, mutable dictionary as
        part of our frozendict. This would be a waste of memory as well as yielding pretty nonsensical semantics wrt
        immutability.
        """
        fd = FrozenDict(a=1)
        with T.assert_raises(TypeError):
            vars(fd)

        with T.assert_raises(AttributeError):
            fd.__dict__

    def test_dunder_init(self):
        fd = FrozenDict(a=1)
        assert fd == {'a': 1}, dict(fd)

        # Implemented naively, __init__ would re-set the value of our immutable object.
        fd.__init__(b=2)
        assert fd == {'a': 1}, dict(fd)


if __name__ == '__main__':
    from testify import run
    run()
