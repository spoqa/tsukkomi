tsukkomi
~~~~~~~~

do `tsukkomi`_ for python types.

.. _tsukkomi: https://en.wikipedia.org/wiki/Glossary_of_owarai_terms#tsukkomi


What is tsukkomi?
=================

tsukkomi is a japanese word means straight man in the comedy duos of western
culture. As straight man react partner's ridiculous behaviors, ``tsukkomi``
will react incorrect types.


How to use tsukkomi?
====================

``tsukkomi`` take type hints from `typing`_. write code with annotation,
decorate all callable objects with ``tsukkomi.typed.typechecked``.
FYI generic types are not supported, see `tsukkomi dosen't support generic`_
section for the detail.


.. code-block:: python

   from typing import Sequence

   from tsukkomi.typed import typechecked

   @typechecked
   def greeting(name: str) -> str:
       return name

   greeting('a') # it is ok
   greeting(1) # this will raise `TypeError`


.. _typing: https://docs.python.org/3/library/typing.html


tsukkomi dosen't support generic
================================

tsukkomi dosen't support `generic`_ type checking, includes types already
inherited a generic type like `typing.Sequence`, `typing.Mutable` and etc.
following example codes can be passed by `tsukkomi.typed.typechecked`.


.. code-block:: python

   import typing

   from tsukkomi.typed import typechecked


   T = typing.TypeVar('T')


   class Boke(typing.Generic[T]):

       @typechecked
       def stupid(self, word: T) -> T:
           return type(word)

       @typechecked
       def correction(self, words: Sequence[T]) -> T:
           return random.sample(words, 1)[0]


   @typechecked
   def boke_and_tsukkomi(stupid_words: Sequence[str],
                         correction: Sequence[str]) -> bool:
       return any(s == c for s, c in zip(stupid_words, correction)))


   boke = Boke[str]()
   print(boke.stupid('hello world'))
   print(boke.correction([1, 2, 3]))
   print(boke_and_tsukkomi([1, 2], [1.0, 2.0]))


.. _generic: https://docs.python.org/3/library/typing.html#user-defined-generic-types
