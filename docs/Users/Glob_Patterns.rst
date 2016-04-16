Glob - Extended unix style pathname expansion
=============================================

In *coala*, files and directories are specified by file name. To allow
input of multiple files without requiring a large number of filenames,
*coala* supports a number of wildcards. These are based on the unix-style
glob syntax and they are *not* the same as regular expressions.

.. note::

    Any glob that does not start with a ``/`` in Linux or a drive letter
    ``X:`` in Windows will be interpreted as a relative path. Please use comma
    separated values instead of absolute path globs that start with a
    glob expression.

Syntax
------

The special characters used in shell-style wildcards are:

+-------------------+---------------------------------------------------------+
| PATTERN           | MEANING                                                 |
+===================+=========================================================+
| ``[seq]``         | Matches any character in seq. Cannot be empty. Any      |
|                   | special character looses its special meaning in a set.  |
+-------------------+---------------------------------------------------------+
| ``[!seq]``        | Matches any character not in seq. Cannot be empty. Any  |
|                   | special character looses its special meaning in a set.  |
+-------------------+---------------------------------------------------------+
| ``(seq_a|seq_b)`` | Matches either sequence_a or sequence_b as a whole. More|
|                   | than two or just one sequence can be given.             |
+-------------------+---------------------------------------------------------+
| ``?``             | Matches any single character.                           |
+-------------------+---------------------------------------------------------+
| ``*``             | Matches everything but the directory separator.         |
+-------------------+---------------------------------------------------------+
| ``**``            | Matches everything.                                     |
+-------------------+---------------------------------------------------------+

Examples
--------

``[seq]``
~~~~~~~~~

    Matches any character in seq. Cannot be empty. Any special character
    looses its special meaning in a set.

Opening and closing brackets can be part of a set, although closing
brackets have to be placed at the first position.

::

    >>> from coalib.parsing.Globbing import fnmatch
    >>> fnmatch("aaa", "a[abc]a")
    True
    >>> fnmatch("aaa", "a[bcd]a")
    False
    >>> fnmatch("aaa", "a[a]]a")
    False
    >>> fnmatch("aa]a", "a[a]]a")
    True
    >>> fnmatch("aaa", "a[]abc]a")
    True
    >>> fnmatch("aaa", "a[[a]a")
    True
    >>> fnmatch("a[a", "a[[a]a")
    True
    >>> fnmatch("a]a", "a[]]a")
    True
    >>> fnmatch("aa", "a[]a")
    False
    >>> fnmatch("a[]a", "a[]a")
    True

``[!seq]``
~~~~~~~~~~

    Matches any character not in seq. Cannot be empty. Any special
    character looses its special meaning in a set.

::

    >>> fnmatch("aaa", "a[!a]a")
    False
    >>> fnmatch("aaa", "a[!b]a")
    True
    >>> fnmatch("aaa", "a[b!b]a")
    False
    >>> fnmatch("a!a", "a[b!b]a")
    True
    >>> fnmatch("a!a", "a[!]a")
    False
    >>> fnmatch("aa", "a[!]a")
    False
    >>> fnmatch("a[!]a", "a[!]a")
    True

``(seq\_a\|seq\_b)``
~~~~~~~~~~~~~~~~~~~~

    Matches either sequence\_a or sequence\_b as a whole. More than two
    or just one sequence can be given.

Parentheses cannot be part of an alternative, unless they are escaped by
brackets. Parentheses that have no match are ignored as well as
``|``-separators that are not inside matching parentheses.

::

    >>> fnmatch("aXb", "a(X|Y)b")
    True
    >>> fnmatch("aYb", "a(X|Y)b")
    True
    >>> fnmatch("aZb", "a(X|Y)b")
    False
    >>> fnmatch("aXb", "(a(X|Y)b|c)")
    True
    >>> fnmatch("c", "(a(X|Y)b|c)")
    True
    >>> fnmatch("a", "a|b")
    False
    >>> fnmatch("a|b", "a|b")
    True
    >>> fnmatch("(a|b", "(a|b")
    True
    >>> fnmatch("(aa", "(a(a|b)")
    True
    >>> fnmatch("a(a", "(a(a|b)")
    False
    >>> fnmatch("a(a", "(a[(]a|b)")
    True
    >>> fnmatch("aa", "a()a")
    True
    >>> fnmatch("", "(abc|)")
    True

``?``
~~~~~

    Matches any single character.

::

    >>> fnmatch("abc", "a?c")
    True
    >>> fnmatch("abbc", "a?c")
    False
    >>> fnmatch("a/c", "a?c")
    True
    >>> fnmatch("a\\c", "a?c")
    True
    >>> fnmatch("a?c", "a?c")
    True
    >>> fnmatch("ac", "a?c")
    False

``\*``
~~~~~~

    Matches everything but the directory separator.

.. note::

    The directory separator is platform specific. ``/`` is never
    matched by ``\*``. ``\\`` is matched on Linux, but not on Windows.

::

    >>> fnmatch("abc", "a*c")
    True
    >>> fnmatch("abbc", "a*c")
    True
    >>> fnmatch("a/c", "a*c")
    False
    >>> fnmatch("a?c", "a*c")
    True
    >>> fnmatch("ac", "a*c")
    True

``\*\*``
~~~~~~~~

    Matches everything.

::

    >>> fnmatch("abc", "a**c")
    True
    >>> fnmatch("abbc", "a**c")
    True
    >>> fnmatch("a/c", "a**c")
    True
    >>> fnmatch("a?c", "a**c")
    True
    >>> fnmatch("ac", "a**c")
    True
