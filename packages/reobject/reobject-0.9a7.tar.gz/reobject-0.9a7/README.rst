reobject
========

|Build Status| |PyPI version| |PyPI| |codecov|

*reobject* is an ORM layer for your objects. It allows you to track and
query objects at runtime using a familiar query langauge inspired by
Django ORM.

**Note:** *reobject* is **NOT** a database ORM. It keeps track of
regular objects in the memory.

**This is highly experimental code, and not safe for production.**

Installation
~~~~~~~~~~~~

*reobject* supports Python 3 only.

.. code:: sh

   pip install reobject

Example usage
~~~~~~~~~~~~~

.. code:: py3

   from reobject.models import Model, Field

   class Book(Model):
       title = Field()
       authors = Field()
       price = Field()

   >>> # Create a bunch of objects
   >>> Book(title='The C Programming Language', authors=['Kernighan', 'Ritchie'], price=52)
   >>> Book(title='The Go Programming Language', authors=['Donovan', 'Kernighan'], price=30)

   >>> Book.objects.all()  # All books
   [Book(title='The C Programming Language', authors=['Kernighan', 'Ritchie'], price=52),
    Book(title='The Go Programming Language', authors=['Donovan', 'Kernighan'], price=30)]

   >>> Book.objects.filter(price__lt=50).values('title')  # Titles of books priced under $50
   [{'title': 'The Go Programming Language'}, {'title': 'The C Programming Language'}]

   >>> # Titles of books co-authored by Brian Kernighan
   >>> Book.objects.filter(authors__contains='Kernighan').values_list('title', flat=True)
   ['The Go Programming Language', 'The C Programming Language']

Features
~~~~~~~~

-  Elegant data-model syntax inspired by Django ORM.
-  Class-level model fields, out of the box object protocols, pretty
   reprs; powered by `attrs <http://attrs.org>`__.
-  Advanced query language and chainable querysets. Read the `QuerySet
   API docs <https://anirudha.co/reobject>`__.
-  Transactions. See
   `example <tests/unit/test_transaction.py#L7-L13>`__.
-  Many-to-one model relationships. See
   `example <tests/unit/test_manager.py#L61-L108>`__
-  [TBA] Attribute indexes for fast lookups.

Crunching Design Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~

+----------+------------------------------------------+------+--------+
| Pattern  | Description                              | Pure | re     |
|          |                                          | Py   | object |
|          |                                          | thon |        |
+==========+==========================================+======+========+
| F        | Reuse existing instances of objects with | `L   | `L     |
| lyweight | identical state                          | ink  | ink <e |
|          |                                          | <htt | xample |
|          |                                          | ps:/ | s/flyw |
|          |                                          | /git | eight. |
|          |                                          | hub. | py>`__ |
|          |                                          | com/ |        |
|          |                                          | faif |        |
|          |                                          | /pyt |        |
|          |                                          | hon- |        |
|          |                                          | patt |        |
|          |                                          | erns |        |
|          |                                          | /blo |        |
|          |                                          | b/ma |        |
|          |                                          | ster |        |
|          |                                          | /str |        |
|          |                                          | uctu |        |
|          |                                          | ral/ |        |
|          |                                          | flyw |        |
|          |                                          | eigh |        |
|          |                                          | t.py |        |
|          |                                          | >`__ |        |
+----------+------------------------------------------+------+--------+
| Memento  | Transactional rollback of an object to a | `Lin | `Link  |
|          | previous state in case of an exception   | k <h |  <test |
|          |                                          | ttps | s/unit |
|          |                                          | ://g | /test_ |
|          |                                          | ithu | transa |
|          |                                          | b.co | ction. |
|          |                                          | m/fa | py>`__ |
|          |                                          | if/p |        |
|          |                                          | ytho |        |
|          |                                          | n-pa |        |
|          |                                          | tter |        |
|          |                                          | ns/b |        |
|          |                                          | lob/ |        |
|          |                                          | mast |        |
|          |                                          | er/b |        |
|          |                                          | ehav |        |
|          |                                          | iora |        |
|          |                                          | l/me |        |
|          |                                          | ment |        |
|          |                                          | o.py |        |
|          |                                          | >`__ |        |
+----------+------------------------------------------+------+--------+
| P        | Create clones of a prototype without     | `L   | `L     |
| rototype | instantiation                            | ink  | ink <e |
|          |                                          | <htt | xample |
|          |                                          | ps:/ | s/prot |
|          |                                          | /git | otype. |
|          |                                          | hub. | py>`__ |
|          |                                          | com/ |        |
|          |                                          | faif |        |
|          |                                          | /pyt |        |
|          |                                          | hon- |        |
|          |                                          | patt |        |
|          |                                          | erns |        |
|          |                                          | /blo |        |
|          |                                          | b/ma |        |
|          |                                          | ster |        |
|          |                                          | /cre |        |
|          |                                          | atio |        |
|          |                                          | nal/ |        |
|          |                                          | prot |        |
|          |                                          | otyp |        |
|          |                                          | e.py |        |
|          |                                          | >`__ |        |
+----------+------------------------------------------+------+--------+
| S        | Restrict a class to provide only a       | `Li  | `L     |
| ingleton | single instance                          | nk < | ink <e |
|          |                                          | http | xample |
|          |                                          | ://p | s/sing |
|          |                                          | ytho | leton. |
|          |                                          | n-3- | py>`__ |
|          |                                          | patt |        |
|          |                                          | erns |        |
|          |                                          | -idi |        |
|          |                                          | oms- |        |
|          |                                          | test |        |
|          |                                          | .rea |        |
|          |                                          | dthe |        |
|          |                                          | docs |        |
|          |                                          | .io/ |        |
|          |                                          | en/l |        |
|          |                                          | ates |        |
|          |                                          | t/Si |        |
|          |                                          | ngle |        |
|          |                                          | ton. |        |
|          |                                          | html |        |
|          |                                          | >`__ |        |
+----------+------------------------------------------+------+--------+
| Facade   | Encapsulate a complex subsystem within a | `Li  | `Link  |
|          | single interface object                  | nk < |  <exam |
|          |                                          | http | ples/f |
|          |                                          | s:// | acade. |
|          |                                          | gith | py>`__ |
|          |                                          | ub.c |        |
|          |                                          | om/f |        |
|          |                                          | aif/ |        |
|          |                                          | pyth |        |
|          |                                          | on-p |        |
|          |                                          | atte |        |
|          |                                          | rns/ |        |
|          |                                          | blob |        |
|          |                                          | /mas |        |
|          |                                          | ter/ |        |
|          |                                          | stru |        |
|          |                                          | ctur |        |
|          |                                          | al/f |        |
|          |                                          | acad |        |
|          |                                          | e.py |        |
|          |                                          | >`__ |        |
+----------+------------------------------------------+------+--------+
| Flux     | Event-driven state management inspired   | `Lin | `Li    |
|          | by Facebook Flux                         | k <h | nk <ex |
|          |                                          | ttps | amples |
|          |                                          | ://g | /flux. |
|          |                                          | ithu | py>`__ |
|          |                                          | b.co |        |
|          |                                          | m/on |        |
|          |                                          | yb/p |        |
|          |                                          | ytho |        |
|          |                                          | n-fl |        |
|          |                                          | ux/b |        |
|          |                                          | lob/ |        |
|          |                                          | mast |        |
|          |                                          | er/f |        |
|          |                                          | lux/ |        |
|          |                                          | stor |        |
|          |                                          | e.py |        |
|          |                                          | >`__ |        |
+----------+------------------------------------------+------+--------+

Note: Some of the examples above may be inaccurate. The idea is to
demonstrate what reobject is capable of. Pull requests are most welcome.

Contributing
~~~~~~~~~~~~

Want to help? You can contribute to the project by:

-  Using reobject in your projects, finding bugs, and proposing new
   features.
-  Sending pull requests with recipes built using reobject.
-  Trying your hand at some `good first
   bugs <https://github.com/onyb/reobject/issues?q=is%3Aissue+is%3Aopen+label%3Abitesize>`__.
-  Improving test coverage, and writing documentation.

.. |Build Status| image:: https://travis-ci.org/onyb/reobject.svg?branch=master
   :target: https://travis-ci.org/onyb/reobject
.. |PyPI version| image:: https://badge.fury.io/py/reobject.svg
   :target: https://badge.fury.io/py/reobject
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/reobject.svg
   :target: https://pypi.python.org/pypi/reobject
.. |codecov| image:: https://codecov.io/gh/onyb/reobject/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/onyb/reobject
