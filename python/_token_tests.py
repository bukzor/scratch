#!/usr/bin/env python
"""tests for the token class"""
# I0011: disabling locally
# C0103: invalid class name
# R0903: too few methods
# R0201: method could be a function
# pylint:disable=I0011,C0103,R0903,R0201

from _token import token
import unittest as T

class TokenTest(T.TestCase):
    """tests for the token class"""
    # R0904: too many methods
    # pylint:disable=R0904
    def test_has_simple_repr(self):
        """token classes should have a simple representation"""
        assert str(token) == "('token',)", str(token)
        # a copy of token
        token2 = token(a=1)
        assert repr(token2) == "('token', {'a': 1})", repr(token2)
        class token3(token):
            """a subclass of `token'"""
            pass
        assert repr(token3) == "('token3',)", str(token3)

    def test_eq(self):
        """Two tokens that are indistinguishable are equal."""
        class Animal(token):
            """A token for animals."""
        a1 = Animal()

        # demo comparison with non-token types
        assert a1 != 'wat'
        assert (a1 == 'wat') is False

        # E0102: class already defined
        # pylint:disable=E0102
        class Animal(token):
            """A somewhat different token for animals."""
        a2 = Animal()

        assert a1 == a2

        a3 = a1(
                token,
                token,
        )

        assert a1 != a3 != a2

        class Animal(Animal):
            """Yet another Animal token."""
            children = (token, token)

        assert a1 != Animal != a2

        assert a3 == Animal()
        assert a1 != Animal() != a2

    def test_subclasses(self):
        """show that token subclasses have good isinstance() behavior"""
        class Animal(token):
            """The Animal token."""
        class Mammal(Animal):
            """A Mammal is an Animal."""

        assert isinstance(Mammal(), Mammal)
        assert isinstance(Animal(), Animal)
        assert isinstance(Mammal(), Animal)

    def test_tree(self):
        """demo the behavior of a token tree"""
        class thing(token):
            """The thing token."""

        tree = thing()
        assert not tree

        tree = thing(
            thing(),
            thing(),
        )

        assert isinstance(tree, token)
        assert isinstance(tree, thing)
        # Demo __len__
        assert len(tree) == 2
        assert tree

        # Demo __iter__
        for child in tree:
            assert isinstance(child, thing)
            assert len(child) == 0
            assert tuple(child) == ()
            assert not child

        tree = tuple(tree)
        assert len(tree) == 2

    def test_default_children(self):
        """show that subclasses can specify default children"""
        class bread(token):
            """A token representing bread."""
        class cheese(token):
            """A token representing cheese."""
        class meat(token):
            """A token representing meat."""

        class Sandwich(token):
            """A token representing a Sandwich."""
            children = (
                bread,
                cheese,
                meat,
                bread,
            )

        class GrilledCheese(Sandwich):
            """A GrilledCheese is a special Sandwich."""
            children = (
                bread,
                cheese,
                bread,
            )

        sandwich = Sandwich()
        assert len(sandwich) == 4

        grilled_cheese = GrilledCheese()
        assert len(grilled_cheese) == 3

        assert isinstance(grilled_cheese, Sandwich)

    def test_default_properties(self):
        class colors(token):
            """a token for colors"""
            properties = {'black':0, 'white':1}

        c = colors()
        assert c.properties == {'black':0, 'white':1}, dict(c.properties)

        c = colors(red=3)
        assert c.properties == {'black':0, 'white':1, 'red':3}, dict(c.properties)

    def test_main(self):
        """Demonstrate some basic token functionalities."""
        class mammal(token):
            """The mammal token."""
        class goat(mammal):
            """A goat is a mammal."""

        assert issubclass(mammal, token)
        assert issubclass(goat, token)
        assert issubclass(goat, mammal)
        assert issubclass(goat, goat)

        assert isinstance(mammal(), token)
        assert isinstance(goat(), token)
        assert isinstance(goat(), mammal)

        assert isinstance(goat(), goat)
        # I got this wrong once.
        assert isinstance(goat(1, 2, 3), goat)

    def test_no_class_attributes(self):
        t = token(token, a=1)
        with assert_raises_exactly(TypeError, 'token objects are read-only'):
            t.properties = {'b':2}

        with assert_raises_exactly(TypeError, 'token objects are read-only'):
            del t.children

    def test_no_object_attributes(self):
        t = token(token, a=1)
        with assert_raises_exactly(TypeError, 'token objects are read-only'):
            t.properties = {'b':2}

        with assert_raises_exactly(TypeError, 'token objects are read-only'):
            del t.children

    def test_class_attrs_immutable(self):
        with assert_raises_exactly(
                TypeError,
                "'FrozenDict' object does not support item assignment",
        ):
            token.properties['b'] = 2

        with assert_raises_exactly(
                AttributeError,
                "'tuple' object has no attribute 'append'",
        ):
            token.children.append('wat')

    def test_object_attrs_immutable(self):
        t = token(token, a=1)
        with assert_raises_exactly(
                TypeError,
                "'FrozenDict' object does not support item assignment",
        ):
            t.properties['b'] = 2

        with assert_raises_exactly(
                AttributeError,
                "'tuple' object has no attribute 'append'",
        ):
            t.children.append('wat')



class QuestionableFeatures(T.TestCase):
    """
    I might decide to delete these features later,
    but this is how they work at this moment.
    """
    def test_copy(self):
        """secondary interface for copying tokens"""
        t1 = token()
        t2 = t1.copy()
        assert t1 == t2, (t1, t2)

    def test_generator_support(self):
        """This will naturally go away if i factor out .copy"""
        t1 = token()
        t3 = t1.copy(children=(token() for i in range(3)))
        assert len(t3.children) == 3
        assert type(t3.children) is tuple

        t4 = t1.copy(properties=((i, i) for i in range(3)))
        assert len(t4.properties) == 3
        from collections import Mapping
        assert isinstance(t4.properties, Mapping)

    def test_default_property_deletion(self):
        class MyToken(token):
            "an example with a default property"
            properties = {'a':1}

        m1 = MyToken()
        assert len(m1.properties) == 1

        m1 = MyToken(a=token.undefined)
        assert len(m1.properties) == 0, dict(m1.properties)


class MetaTokenTest(T.TestCase):
    """Disabled test for tokenType"""
    __test__ = True
    def test_issubclass(self):
        """Demonstrate issubclass behavior with tokenType."""
        class mammal(token):
            """The mammal token."""
        class goat(mammal):
            """A goat is a mammal."""

        assert repr(token) == repr(token())
        assert type.mro(token) == type.mro(token())[1:]

        assert issubclass(mammal(), token)
        assert issubclass(goat(), token)
        assert issubclass(goat(), mammal)

        assert issubclass(goat(), goat)
        # I got this wrong once.
        assert issubclass(goat(1, 2, 3), goat)
        assert not issubclass(goat(1, 2, 3), goat(1, 2))

        assert goat == goat()

    def test_repr(self):
        """token classes should have a simple representation"""
        assert str(token) == "('token',)"
        # a copy of token
        token2 = token(a=1)
        assert repr(token2) == "('token', {'a': 1})", repr(token2)
        class token3(token):
            """a subclass of `token'"""
            pass
        assert repr(token3) == "('token3',)"

    def test_eq(self):
        """Two tokens that are indistinguishable are equal."""
        class Animal(token):
            """A token for animals."""
        a1 = Animal
        # E0102: class already defined
        # pylint:disable=E0102
        class Animal(token):
            """A somewhat different token for animals."""
        a2 = Animal

        assert a1 == a2

        a3 = a1(
                token,
                token,
        )

        assert a1 != a3 != a2

        class Animal(Animal):
            """Yet another Animal token."""
            children = (token, token)

        assert a3 == Animal
        assert a1 != Animal != a2

        assert a3 == Animal()
        assert a1 != Animal() != a2

from contextlib import contextmanager
@contextmanager
def assert_raises_exactly(exception_type, *args, **attrs):
    try:
        yield
    except Exception, exception:
        assert type(exception) is exception_type, type(exception)
        assert exception.args == args, exception.args
        assert exception.__dict__ == attrs, exception.__dict__
    else:
        raise AssertionError('No exception raised!')


if __name__ == '__main__':
    import pytest
    import sys
    exit(pytest.main(sys.argv))
