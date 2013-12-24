#!/usr/bin/env python
# I0011: disabling locally
# C0301: line too long
# W0111: missing docstring
# C0103: invalid class name
# pylint:disable=I0011,C0301,C0111,C0103

from _token import token

def test_subclasses():
    class Animal(token):
        pass
    class Mammal(Animal):
        pass

    assert isinstance(Mammal(), Mammal)
    assert isinstance(Animal(), Animal)
    assert isinstance(Mammal(), Animal)

def test_tree():
    class thing(token):
        pass

    tree = thing()
    assert not tree

    tree = thing(
        thing(),
        thing(),
    )

    assert isinstance(tree, token)
    assert isinstance(tree, thing)
    assert len(tree) == 2
    assert tree

    tree = tuple(tree)
    assert len(tree) == 2
    for child in tree:
        assert isinstance(child, thing)
        assert len(child) == 0
        assert tuple(child) == ()
        assert not child

def test_default_children():
    class bread(token):
        pass
    class cheese(token):
        pass
    class meat(token):
        pass

    class Sandwich(token):
        children = (
            bread,
            cheese,
            meat,
            bread,
        )

    class GrilledCheese(Sandwich):
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


def test_main():
    class mammal(token):
        pass
    class goat(mammal):
        pass


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
