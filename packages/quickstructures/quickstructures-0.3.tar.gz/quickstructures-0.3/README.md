
Quickstructures
===============

These are some handy functions that allow you to create anonymous objects with
convenience.


They are wrappes for creating [namedtuple](http://docs.python.org/2/library/collections.html#collections.namedtuple)s.

Examples
========

    > struct(x = 1, y = 2)
    Struct(y=2, x=1)

    > nstruct('Point').of(x = 1, y = 2)
    Point(y=2, x=1)

    > struct(x = 1, y = 2) == struct(y = 2, x = 1)
    True

    > struct(x = 1, y = 2) == struct(y = 2, x = 3)
    False

