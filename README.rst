``csvprint``
============

|Build Status|

Command-line utility for pretty printing csv files.

Example
-------

::

    » csvprint imdb.csv
    Title                  Release Year Estimated Budget
    Shawshank Redemption   1994         $25 000 000
    The Godfather          1972         $6 000 000
    The Godfather: Part II 1974         $13 000 000
    The Dark Knight        2008         $185 000 000
    12 Angry Men           1957         $350 000

You can also pipe output from other programs to csvprint to format the
output:

::

    » cat imdb.csv | csvprint
    Title                  Release Year Estimated Budget
    Shawshank Redemption   1994         $25 000 000
    The Godfather          1972         $6 000 000
    The Godfather: Part II 1974         $13 000 000
    The Dark Knight        2008         $185 000 000
    12 Angry Men           1957         $350 000

Installation
------------

Clone the repo and do ``pip install .``, and you should be good to go.

Flags
-----

-  ``--markdown`` produces a markdown table. If you just want this,
   though, you should probably use
   ```csvtomd`` <https://github.com/mplewis/csvtomd>`__.
-  ``-s`` to specify delimiter (default is comma), in case of e.g. a
   tab-separated file
-  ``-n`` to specify number of rows to show
-  ``j`` or ``--justify`` to specify justification (left or right). See
   examples below
-  ``-d`` decorator to separate fields by (e.g. ``' '``, which is
   default)
-  ``--header`` add border around the header (first line)
-  ``--padding`` add padding to each side of columns (default is 1)

Justification
-------------

There are three options for specifying justification. One can use ``l``
or ``r`` for justifying all cells to the left or right, respectively.
One can also specify a distinct justification option for each column.
Then the number of options will need to match the number of columns.

::

    » csvprint imdb.csv -j l r r
    Title                  Release Year Estimated Budget
    Shawshank Redemption           1994      $25 000 000
    The Godfather                  1972       $6 000 000
    The Godfather: Part II         1974      $13 000 000
    The Dark Knight                2008     $185 000 000
    12 Angry Men                   1957         $350 000

Markdown example
----------------

Note that this also supports left and right justification (not centered
for now).

::

    » csvprint imdb.csv --markdown
    Title                  | Release Year | Estimated Budget
    :----------------------|:-------------|:----------------
    Shawshank Redemption   | 1994         | $25 000 000
    The Godfather          | 1972         | $6 000 000
    The Godfather: Part II | 1974         | $13 000 000
    The Dark Knight        | 2008         | $185 000 000
    12 Angry Men           | 1957         | $350 000

When rendered as markdown, this looks like

+--------------------------+----------------+--------------------+
| Title                    | Release Year   | Estimated Budget   |
+==========================+================+====================+
| Shawshank Redemption     | 1994           | $25 000 000        |
+--------------------------+----------------+--------------------+
| The Godfather            | 1972           | $6 000 000         |
+--------------------------+----------------+--------------------+
| The Godfather: Part II   | 1974           | $13 000 000        |
+--------------------------+----------------+--------------------+
| The Dark Knight          | 2008           | $185 000 000       |
+--------------------------+----------------+--------------------+
| 12 Angry Men             | 1957           | $350 000           |
+--------------------------+----------------+--------------------+

Help message
------------

``csvprint -h`` or ``csvprint --help`` prints a help message:

::

    » csvprint -h
    usage: csvprint [-h] [-s SEPARATOR] [-n ROWS] [-j JUSTIFY [JUSTIFY ...]]
                    [-d DECORATOR] [-p PADDING] [--header | --markdown]
                    [filename]

    Command line utility for pretty printing csv files.

    positional arguments:
      filename              file to pretty print

    optional arguments:
      -h, --help            show this help message and exit
      -s SEPARATOR, --separator SEPARATOR
                            separator/delimiter used in csv file
                            default is comma
                            use 'tab' for tab separated files
      -n ROWS, --rows ROWS  number of rows to show
      -j JUSTIFY [JUSTIFY ...], --justify JUSTIFY [JUSTIFY ...]
                            which justification to use
                            default is left
                            choices: {l, r}
                            can provide a list, in which case
                            one choice for each column
      -d DECORATOR, --decorator DECORATOR
                            which string/decorator to use in spacing
      -p PADDING, --padding PADDING
                            padding
      --header              header decoration
      --markdown            output markdown table

Testing
-------

Run ``pytest`` while in the root directory of this repository.

.. |Build Status| image:: https://travis-ci.org/vegarsti/csvprint.svg?branch=master
   :target: https://travis-ci.org/travis-ci/travis-web
