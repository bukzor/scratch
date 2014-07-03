# pylint:disable=missing-docstring,too-few-public-methods,no-init,invalid-name
from classobject2 import Class, Object
from _token import tokenType, token


class DummyObject(object):
    def __init__(self, **attrs):
        self.__dict__.update(attrs)


def pytest_generate_tests(metafunc):
    if 'classobj' in metafunc.fixturenames:
        metafunc.parametrize(
            "type_,classobj", [
                (Class, Object),
                (tokenType, token),
            ],
        )
    else:
        metafunc.parametrize(
            "type_,class_", [
                (type, object),
                (Class, Object),
                (tokenType, token),
            ],
        )


def assert_instance(type_, class_, obj, **attrs):
    for attr, val in attrs.items():
        assert getattr(obj, attr) == val

    assert type(obj) is class_
    assert type(type(obj)) is type_


def test_instantiate(type_, class_, **attrs):
    obj = class_()

    assert_instance(type_, class_, obj, **attrs)


def test_class_type(type_, class_):
    assert type(class_) is type_


def test_subclassing(type_, class_):
    class subclass(class_):
        one = 1

        @property
        def two(self):
            assert type(self) is subclass
            return 2

        @staticmethod
        def three():
            return 3

        @classmethod
        def four(cls):
            assert cls is subclass
            return 4

        def five(self):
            assert type(self) is subclass
            return 5

    assert subclass.one == 1

    obj = subclass()
    assert obj.one == 1
    assert obj.two == 2
    assert obj.three() == 3
    assert obj.four() == 4
    assert obj.five() == 5

    assert issubclass(subclass, class_)

    test_instantiate(type_, subclass)
    test_class_type(type_, subclass)
    assert_instance(type(type_), type_, subclass)


def test_instantiate_a_subclass(type_, class_):
    class subclass2(class_):
        one = 1

        @property
        def two(self):
            assert type(self) is subclass2
            return 2

    obj = subclass2()

    assert_instance(type_, subclass2, obj, one=1, two=2)


def test_subclass_a_subclass(type_, class_):
    class subclass3(class_):
        @property
        def one(self):
            assert type(self) is subclass3
            return 2

        two = 1

    test_subclassing(type_, subclass3)


def test_subclass_a_classobj(type_, classobj):
    del type_
    subclass = classobj()

    test_subclassing(classobj, subclass)


def test_classobj_properties(type_, classobj):
    class subclass4(classobj):
        one = 1

        @property
        def two(self):
            assert issubclass(self, subclass4)
            return 2

    assert_instance(
        type,
        type_,
        subclass4,
        one=1,
        two=2,
    )
