""":mod:`tsukkomi.typed` --- A functions check types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import functools
import inspect
import itertools
import types
import typing

__all__ = (
    'check_arguments', 'check_callable', 'check_return', 'check_tuple',
    'check_type', 'check_union', 'typechecked',
)


T = typing.TypeVar('T')
NoneType = type(None)


def check_type(value: typing.Any, hint: typing.Optional[type]) -> bool:
    """Check given ``value``'s type.

    :param value: given argument
    :param hint: expected type of given ``value``.
                 as like :mod:`typing` interprets, :const:`None` is interpreted
                 as :class:`types.NoneType`
    :type hint: :class:`typing.Optional`[:class:`type`]

    """
    if hint is None:
        hint = NoneType
    actual_type = type(value)
    if hint is NoneType:
        correct = value is None
    elif hint is typing.Any:
        correct = True
    elif hint is typing.Pattern or hint is typing.Match:
        correct = isinstance(value, hint.impl_type)
    elif isinstance(hint, typing.TypeVar):
        # TODO: Check generic
        correct = True
    elif issubclass(hint, typing.Callable):
        actual_type, correct = check_callable(value, hint)
    elif issubclass(hint, typing.Tuple):
        actual_type, correct = check_tuple(value, hint)
    elif issubclass(hint, typing.Union):
        actual_type, correct = check_union(value, hint)
    else:
        correct = isinstance(value, hint)
    return actual_type, correct


def check_return(callable_name: str, r: typing.Any,
                 hints: typing.Mapping[str, type]) -> None:
    """Check return type, raise :class:`TypeError` if return type is not
    expected type.

    :param str callable_name: callable name of :func:`~.typechecked` checked
    :param r: returned result
    :param hints: assumed type of given ``r``

    """
    correct = True
    if 'return' not in hints:
        return
    _, correct = check_type(r, hints['return'])
    if not correct:
        raise TypeError(
            'Incorrect return type `{}`, expected {}. for: {}'.format(
                type(r), hints.get('return'), callable_name
            )
        )


def check_callable(callable_: typing.Callable, hint: type) -> bool:
    """Check argument type & return type of :class:`typing.Callable`. since it
    raises check :class:`typing.Callable` using `isinstance`, so compare in
    diffrent way

    :param callable_: callable object given as a argument
    :param hint: assumed type of given ``callable_``

    """
    if not callable(callable_):
        return type(callable_), False
    if callable(callable_) and not hasattr(callable_, '__code__'):
        return type(callable_), True
    hints = typing.get_type_hints(callable_)
    return_type = hints.pop('return', type(None))
    signature = inspect.signature(callable_)
    arg_types = tuple(
        param.annotation
        for _, param in signature.parameters.items()
    )
    correct = all({
        any({
            hint.__args__ is None,
            hint.__args__ is Ellipsis,
            hint.__args__ == arg_types,
        }),
        any({
            hint.__result__ is None,
            hint.__result__ in (typing.Any, return_type)
        })
    })
    return typing.Callable[list(arg_types), return_type], correct


def check_tuple(data: typing.Tuple, hint: type) -> bool:
    """Check argument type & return type of :class:`typing.Tuple`. since it
    raises check :class:`typing.Tuple` using `isinstance`, so compare in
    diffrent way

    :param data: tuple given as a argument
    :param hint: assumed type of given ``data``

    """
    tuple_param = hint.__tuple_params__
    if len(data) != len(tuple_param):
        raise TypeError('expected tuple size is {},'
                        'found: {}'.format(len(tuple_param), len(data)))
    zipped = itertools.zip_longest(data, tuple_param)
    for i, (v, t) in enumerate(zipped):
        _, correct = check_type(v, t)
        if not correct:
            raise TypeError(
                '{0}th item `{1}` in tuple must be {2!r}, not: {3!r}'.format(
                    i, v, t, v
                )
            )
    return hint, True


def check_union(data: typing.Union, hint: type) -> bool:
    """Check argument type & return type of :class:`typing.Union`. since it
    raises check :class:`typing.Union` using `isinstance`, so compare in
    diffrent way

    :param data: union given as a argument
    :param hint: assumed type of given ``data``

    """
    r = any(check_type(data, t)[1] for t in hint.__union_params__)
    if not r:
        raise TypeError(
            'expected one of {0!r}, found: {1!r}'.format(
                hint.__union_params__, type(data)
            )
        )
    return hint, r


def check_arguments(c: typing.Callable,
                    hints: typing.Mapping[str, typing.Optional[type]],
                    *args, **kwargs) -> None:
    """Check arguments type, raise :class:`TypeError` if argument type is not
    expected type.

    :param c: callable object want to check types
    :param hints: assumed type of given ``c`` result of
                  :func:`typing.get_type_hints`

    """
    signature = inspect.signature(c)
    bound = signature.bind(*args, **kwargs)
    for argument_name, value in bound.arguments.items():
        try:
            type_hint = hints[argument_name]
        except KeyError:
            continue
        actual_type, correct = check_type(value, type_hint)
        if not correct:
            raise TypeError(
                'Incorrect type `{}`, expected `{}` for `{}`'.format(
                    actual_type, type_hint, argument_name
                )
            )


def typechecked(call_: typing.Callable[..., T]) -> T:
    """A decorator to make a callable object checks its types

    .. code-block:: python

       from typing import Callable

       @typechecked
       def foobar(x: str) -> bool:
           return x == 'hello world'


       @typechecked
       def hello_world(foo: str, bar: Callable[[str], bool]) -> bool:
           return bar(foo)


       hello_world('hello world', foobar)
       hello_world(3.14, foobar) # it raise TypeError


    :param c: callable object want to check types
    :type c: :class:`typing.Callable`
    :return:

    """
    @functools.wraps(call_)
    def decorator(*args, **kwargs):
        hints = typing.get_type_hints(call_)
        check_arguments(call_, hints, *args, **kwargs)
        result = call_(*args, **kwargs)
        check_return(call_.__name__, result, hints)
        return result

    return decorator
