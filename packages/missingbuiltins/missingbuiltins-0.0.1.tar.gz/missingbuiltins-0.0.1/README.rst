.. image:: https://img.shields.io/pypi/v/missingbuiltins.svg
        :target: https://pypi.python.org/pypi/missingbuiltins

.. image:: https://img.shields.io/travis/jbn/missingbuiltins.svg
        :target: https://travis-ci.com/jbn/missingbuiltins

====
What
====

Code I write over and over for no good reason.

Gonna see what happens by means of accretion.

------------
Installation
------------

.. code-block:: bash

   pip install missingbuiltins

-----
Usage
-----

.. code-block:: python

   from missingbuiltins import jsonl_load, jsonl_dump, chunker

   items = chunker(range(5), 2)
   jsonl_dumps("my_items.jsonl", items)  # => 5
   got = list(jsonl_load(my_items))  # => [[1, 2], [3, 4], [5]]


