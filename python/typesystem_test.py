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


def test_class_type(type_, class_):
    assert type(class_) is type_


def test_obj_type(type_, class_):
    obj = class_()
    assert type(obj) is class_
    assert type(type(obj)) is type_


def test_subclass(type_, class_):
    class subclass(class_):
        pass

    assert issubclass(subclass, class_)

    test_class_type(type_, subclass)
    test_obj_type(type_, subclass)


if True:
    def test_instantiate_a_classobj(type_, classobj):
        A = classobj()
        test_obj_type(classobj, A)
else:
    def test_subclass_a_classobj(type_, classobj):
        A = classobj()

        test_subclass(type_, A)
