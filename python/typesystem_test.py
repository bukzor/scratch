# pylint:disable=missing-docstring,too-few-public-methods,no-init,invalid-name
from classobject2 import Class, Object


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


def assert_instance(type_, class_, obj):
    assert type(obj) is class_
    assert type(type(obj)) is type_


def test_obj_type(type_, class_):
    obj = class_()

    assert_instance(type_, class_, obj)


def test_class_type(type_, class_):
    assert type(class_) is type_


def assert_subclass(type_, class_, subclass):
    assert issubclass(subclass, class_)

    test_obj_type(type_, subclass)
    test_class_type(type_, subclass)


def test_subclass(type_, class_):
    class subclass(class_):
        pass

    assert_subclass(type_, class_, subclass)


def test_instantiate_a_subclass(type_, class_):
    class subclass(class_):
        pass

    obj = subclass()

    assert_instance(type_, subclass, obj)


def test_subclass_a_subclass(type_, class_):
    class subclass(class_):
        pass

    test_subclass(type_, subclass)


def test_subclass_a_classobj(type_, classobj):
    subclass = classobj()

    test_subclass(classobj, subclass)
