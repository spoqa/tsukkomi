tsukkomi
~~~~~~~~

do `tsukkomi`_ for python types.

.. _tsukkomi: https://en.wikipedia.org/wiki/Glossary_of_owarai_terms#tsukkomi


Why do i need tsukkomi?
=======================

tsukkomi is a japanese word means straight man in the comedy duos of western
culture. As straight man react partner's ridiculous behaviors, ``tsukkomi``
will react incorrect types.


How to use tsukkomi?
====================

``tsukkomi`` take type hints from `typing`_. write code with annotation,
decorate all callable objects with ``tsukkomi.typed.typechecked``.

.. code-block:: python

   from typing import Sequence

   from tsukkomi.typed import typechecked

   @typechecked
   def greeting(names: Sequence[str]) -> str:
       return names[0]

   greeting(['a']) # it is ok
   greeting([1]) # this will raise `TypeError`


.. _typing: https://docs.python.org/3/library/typing.html


tsukkomi dosen't support
========================

- `generic`_ type check


.. _generic: https://docs.python.org/3/library/typing.html#user-defined-generic-types
