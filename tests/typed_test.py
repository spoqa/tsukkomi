import re
import typing

from pytest import raises

from tsukkomi.typed import typechecked

T = typing.TypeVar('T')


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
def check_sequence(a: typing.Sequence[int]) -> int:
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
def check_callable(f: typing.Callable[[], str]) -> str:
    return f()


class TestCls(object):

    pass


@typechecked
def check_callable_cls(f: typing.Callable) -> str:
    assert f()
    return 'hello world'


def test_callable():
    assert check_callable(_call)
    with raises(TypeError):
        check_callable('not callable')
    with raises(TypeError):
        check_callable(TestCls)
    check_callable_cls(TestCls)


def _call2(x: str, y: int) -> bool:
    return x == 'a'


@typechecked
def check_callable2(f: typing.Callable[[str, int], bool]) -> str:
    return 'o' if f('1', 2) else 'x'


def test_callable_has_arguments():
    assert check_callable2(_call2)


def _call3(g: typing.Callable[[float], float]) -> bool:
    return g(1.1) == 1.1


def x(a: float) -> float:
    return a


@typechecked
def check_callable3(
    f: typing.Callable[[typing.Callable[[float], float]], bool]
) -> str:
    return 'o' if f(x) else 'x'


def test_callable_has_callable_argument():
    assert check_callable3(_call3)


@typechecked
def check_callable4(f: typing.Callable) -> str:
    return 'o' if f(x) else 'x'


@typechecked
def check_callable5(f: typing.Callable[..., typing.Any]) -> str:
    return 'o' if f(x) else 'x'


def test_callable_without_any_filters():
    assert check_callable4(lambda x: True) == 'o'
    assert check_callable5(lambda x: False) == 'x'


class Human(object):

    @typechecked
    def say(self, word: str) -> str:
        return word


def test_method():
    human = Human()
    assert human.say('world')
    with raises(TypeError):
        assert human.say(1)


@typechecked
def check_set(a: typing.Set[int]) -> typing.Set[int]:
    return a


def test_set():
    assert check_set({1, 2})
    with raises(TypeError):
        assert check_set(1.2)


@typechecked
def check_frozenset(a: typing.FrozenSet[int]) -> typing.FrozenSet[int]:
    return a


def test_frozenset():
    assert check_frozenset(frozenset({1, 2}))
    with raises(TypeError):
        assert check_frozenset(1.2)
    with raises(TypeError):
        assert check_frozenset({1, 2})


@typechecked
def check_mutableset(a: typing.MutableSet[int]) -> typing.MutableSet[int]:
    return a


def test_mutableset():
    assert check_mutableset({1, 2})
    with raises(TypeError):
        assert check_mutableset(frozenset({1, 2}))


@typechecked
def check_dict(a: typing.Dict[str, str]) -> typing.Dict[str, str]:
    return a


def test_dict():
    assert check_dict({'a': 'b'})
    with raises(TypeError):
        assert check_dict(1)


class fakedict(dict):

    def items(self) -> str:
        return 'helloworld'

    def keys(self) -> str:
        return 'foobar'

    def values() -> str:
        return 'lorem ipsum'


@typechecked
def check_itemview(a: typing.Dict[str, str]) -> typing.ItemsView:
    return a.items()


def test_itemview():
    assert check_itemview({'a': 'b'})
    with raises(TypeError):
        assert check_itemview(fakedict(a='b'))


@typechecked
def check_keysview(a: typing.Dict[str, str]) -> typing.KeysView:
    return a.keys()


def test_keysview():
    assert check_keysview({'a': 'b'})
    with raises(TypeError):
        assert check_keysview(fakedict(a='b'))


@typechecked
def check_valuesview(a: typing.Dict[str, str]) -> typing.ValuesView:
    return a.values()


def test_valuesview():
    assert check_valuesview({'a': 'b'})
    with raises(TypeError):
        assert check_valuesview(fakedict(a='b'))


class CheckGeneric(typing.Generic[T]):

    @typechecked
    def check(self, a: T) -> T:
        return True


def test_generic_pass_everything():
    # TODO: Support generic type checking
    cg = CheckGeneric[int]()
    assert cg.check('asc')


@typechecked
def check_generator() -> typing.Generator:
    for y in range(1, 10):
        yield y


@typechecked
def check_generator_fail() -> typing.Generator:
    return 1


def test_generator():
    assert check_generator()
    with raises(TypeError):
        assert check_generator_fail()


@typechecked
def check_tuple(a: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
    return a


def test_typing_tuple():
    assert check_tuple((1, 2))
    with raises(TypeError):
        assert check_tuple(1)


@typechecked
def check_union(a: typing.Union[int, float]) -> typing.Union[int, float]:
    return a


def test_union():
    assert check_union(1)
    assert check_union(1.2)
    with raises(TypeError):
        assert check_union('ss')


@typechecked
def check_optional(a: typing.Optional[int]) -> typing.Optional[int]:
    return a


def test_optional():
    assert check_optional(1)
    assert check_optional(None) is None
    with raises(TypeError):
        # typing.Optional[int] == typing.Union[int, None]
        assert check_optional('ss')


@typechecked
def check_list(a: typing.List) -> typing.List:
    return a


def test_list():
    assert check_list([1, 2])
    with raises(TypeError):
        assert check_list(1)


@typechecked
def check_iterable(a: typing.Iterable) -> typing.Iterable:
    return a


def test_iterable():
    assert check_iterable([1, 2])
    assert check_iterable((1, 2))
    assert check_iterable({1, 2})
    assert check_iterable(frozenset({1, 2}))
    assert check_iterable({'a': 2}.items())
    assert check_iterable({'a': 2}.keys())
    assert check_iterable({'a': 2}.values())
    assert check_iterable('abcdef')
    assert check_iterable(check_generator())
    with raises(TypeError):
        assert check_iterable(1)


@typechecked
def check_mapping(a: typing.Mapping) -> typing.Mapping:
    return a


def test_mapping():
    assert check_mapping({1: 2})
    with raises(TypeError):
        assert check_mapping(1)


@typechecked
def check_pattern(a: typing.Pattern) -> typing.Pattern:
    return a


def test_pattern():
    assert check_pattern(re.compile('[a-z]'))
    with raises(TypeError):
        assert check_pattern(1)


@typechecked
def check_match(a: typing.Match) -> typing.Any:
    return a


def test_match():
    assert check_match(re.match('[a-z]', 'a'))
    with raises(TypeError):
        assert check_match(1)


@typechecked
def check_none_cls(a: type(None)):
    return a


def test_none_cls():
    assert check_none_cls(None) is None
    with raises(TypeError):
        check_none_cls(123)


@typechecked
def check_none(a: None):
    return a


def test_none():
    assert check_none(None) is None
    with raises(TypeError):
        check_none(123)
