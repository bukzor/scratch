#!/usr/bin/env python
"""tests for the token class"""
# I0011: disabling locally
# C0111: missing docstring
# C0103: invalid class name
# pylint:disable=I0011,C0103

from _token import token
from unittest import TestCase

class TokenTests(TestCase):
    """tests for the token class"""
    # R0904: too many methods
    # R0201: method could be a function
    # pylint:disable=R0904,R0201
    def test_has_simple_repr(self):
        """token classes should have a simple representation"""
        assert str(token) == "('token',)"
        # a copy of token
        token2 = token(a=1)
        assert repr(token2),"('token',)"
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

        class Animal(a2):
            """Yet another Animal token."""
            children = (token, token)

        assert a3 == Animal
        assert a1 != Animal != a2

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

        tree = tuple(tree)
        assert len(tree) == 2
        # Demo __iter__
        for child in tree:
            assert isinstance(child, thing)
            assert len(child) == 0
            assert tuple(child) == ()
            assert not child

    def test_default_children(self):
        """show that subclasses can specify default children"""
        class bread(token):
            """The bread token."""
        class cheese(token):
            """The cheese token."""
        class meat(token):
            """The meat token."""

        class Sandwich(token):
            """The Sandwich token."""
            children = (
                bread,
                cheese,
                meat,
                bread,
            )

        class GrilledCheese(Sandwich):
            """The GrilledCheese token."""
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


    def test_main(self):
        """Demonstrate some basic token functionalities."""
        class mammal(token):
            """The mammal token."""
        class goat(mammal):
            """A goat is a mammal."""


        assert repr(token) == repr(token())
        assert type.mro(token) == type.mro(token())[1:]

        assert issubclass(mammal, token)
        assert issubclass(mammal(), token)
        assert issubclass(goat, token)
        assert issubclass(goat(), token)
        assert issubclass(goat, mammal)
        assert issubclass(goat(), mammal)

        assert issubclass(goat, goat)
        assert issubclass(goat(), goat)
        # I got this wrong once.
        assert issubclass(goat(1, 2, 3), goat)
        assert not issubclass(goat(1, 2, 3), goat(1, 2))

        assert goat == goat()

if __name__ == '__main__':
    import pytest
    import sys
    exit(pytest.main(sys.argv))
