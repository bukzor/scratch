# pylint:disable=missing-docstring,too-few-public-methods,no-init,invalid-name
from classobject2 import Class, Object


class DummyObject(object):
    def __init__(self, **attrs):
        self.__dict__.update(attrs)


def pytest_generate_tests(metafunc):
    if 'classobj' in metafunc.fixturenames:
        metafunc.parametrize(
            "type_,classobj", [
                (Class, Object),
            ],
        )
    else:
        metafunc.parametrize(
            "type_,class_", [
                (type, object),
                (Class, Object),
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


def assert_subclass(type_, class_, subclass, **attrs):
    assert issubclass(subclass, class_)

    test_instantiate(type_, subclass)
    test_class_type(type_, subclass)


def test_subclassing(type_, class_):
    class subclass(class_):
        one = 1

        @property
        def two(self):
            return 2

    assert_subclass(type_, class_, subclass, one=1, two=2)


def test_instantiate_a_subclass(type_, class_):
    class subclass(class_):
        pass

    obj = subclass()

    assert_instance(type_, subclass, obj)


def test_subclass_a_subclass(type_, class_):
    class subclass(class_):
        pass

    test_subclassing(type_, subclass)


def test_subclass_a_classobj(type_, classobj):
    subclass = classobj()

    test_subclassing(classobj, subclass)