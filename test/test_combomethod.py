
from combomethod import *
import pytest


def test_basic():
    """
    Ensure that a @combomethod can be called from either a class
    or an instance equally.
    """

    class A(object):

        @combomethod
        def either(receiver, x, y):
            return x + y

    a = A()
    assert a.either(1, 3) == 4
    assert A.either(1, 3) == 4


def test_expected_receiver():
    """
    Ensure receiver is exactly the object or type of object expected.
    """

    class Combo(object):

        @combomethod
        def meth_with_instance(receiver, x, y):
            assert isinstance(receiver, Combo)
            return x + y

        @combomethod
        def meth_with_class(receiver, x, y):
            assert isinstance(receiver, type)
            assert receiver is Combo
            return x + y

    assert Combo.meth_with_class(44, 66) == 110
    c = Combo()
    assert c.meth_with_instance(44, 66) == 110


def test_extended_example():
    """
    Now a real usage, where class and instance vars are essential.
    """

    class Above(object):

        base = 10

        def __init__(self, base=100):
            self.base = base

        @combomethod
        def above_base(receiver, x):
            return receiver.base + x

    a = Above()
    assert a.above_base(5) == 105
    assert Above.above_base(5) == 15

    aa = Above(12)
    assert aa.above_base(5) == 17
    assert Above.above_base(5) == 15


def test_combomethod_useful():
    """
    Demonstration that @combomethod is useful. You cannot in pure Python
    have an instance method that takes either a class or instance receiver,
    without throwing an error. It's possible to use @classmethod as a
    "poor man's @combomethod," but unlike ``@staticmethod`` and
    ``@classmethod``, doesn't clearlly delinate the purpose of the
    decoration.
    """

    class B(object):

        def meth(self, x, y):
            return x + y

        @classmethod
        def cmeth(cls, x, y):
            return x + y

        @classmethod
        def cmeth_never_self(receiver, x, y):
            assert isinstance(receiver, B)      # fails

    # the "normal cases"
    b = B()
    assert b.meth(2, 5) == 7
    assert B.cmeth(2, 5) == 7

    # proof you can't call an intstance method with a class
    with pytest.raises(TypeError):
        B.meth(1, 3)

    # you can, however, call a classmethod with an instance
    b = B()
    assert b.cmeth(1, 3) == 4

    # But it won't work like you want, because the first argument will
    # always be a class, not an instance. I.e., you can never get the proper
    # ``self``.
    with pytest.raises(AssertionError):
        b.cmeth_never_self(1, 3)
