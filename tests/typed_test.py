from typing import Callable, Sequence, TypeVar

from pytest import raises

from tsukkomi.typed import typechecked

T = TypeVar('T')


@typechecked
def greeting(a: str='', b: int=0, c: float=0.0) -> str:
    return 'hello'


def test_check_argument_primitive():
    with raises(TypeError):
        assert greeting(3.14)

    with raises(TypeError):
        assert greeting(a=3.14)

    with raises(TypeError):
        assert greeting(b='a')

    with raises(TypeError):
        assert greeting(c=1)


@typechecked
def return_weird() -> str:
    return True


def test_return_argument_primitive():
    with raises(TypeError):
        assert return_weird()


@typechecked
def return_dosent_have_annotation():
    return True


def test_return_argument_primitive_dosent_have_return_type():
    assert return_dosent_have_annotation()


@typechecked
def check_sequence(a: Sequence[int]) -> int:
    return a[0]


def test_check_sequence():
    with raises(TypeError):
        assert check_sequence({})


def test_check_sequence_with_wrong_argument():
    with raises(TypeError):
        assert check_sequence(['a'])


def _call() -> str:
    return 'a'


@typechecked
def check_callable(f: Callable[[], str]) -> str:
    return f()


def test_callable():
    assert check_callable(_call)


def _call2(x: str, y: int) -> bool:
    return x == 'a'


@typechecked
def check_callable2(f: Callable[[str, int], bool]) -> str:
    return 'o' if f('1', 2) else 'x'


def test_callable_has_arguments():
    assert check_callable2(_call2)


def _call3(g: Callable[[float], float]) -> bool:
    return g(1.1) == 1.1


def x(a: float) -> float:
    return a


@typechecked
def check_callable3(f: Callable[[Callable[[float], float]], bool]) -> str:
    return 'o' if f(x) else 'x'


def test_callable_has_callable_argument():
    assert check_callable3(_call3)


class Human(object):

    @typechecked
    def say(self, word: str) -> str:
        return word


def test_method():
    human = Human()
    assert human.say('world')
    with raises(TypeError):
        assert human.say(1)
