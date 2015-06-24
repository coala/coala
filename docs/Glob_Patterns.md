# Glob - Extended unix style pathname expansion

In coala, files and directories are specified by file name. To allow input of
multiple files without requiring a large number of filenames, coala supports
a number of wildcards. These are based on the unix-style glob syntax and they
are *not* the same as regular expressions.

## Syntax

The special characters used in shell-style wildcards are:

```
+-----------------+-----------------------------------------------------------+
| PATTERN         | MEANING                                                   |
+=================+===========================================================+
| '[seq]'         | Matches any character in seq. Cannot be empty. Any special|
|                 | character looses its special meaning in a set.            |
+-----------------+-----------------------------------------------------------+
| '[!seq]'        | Matches any character not in seq. Cannot be empty. Any    |
|                 | special character looses its special meaning in a set.    |
+-----------------+-----------------------------------------------------------+
| '(seq_a|seq_b)' | Matches either sequence_a or sequence_b as a whole. More  |
|                 | than two or just one sequence can be given.               |
+-----------------+-----------------------------------------------------------+
| '?'             | Matches any single character.                             |
+-----------------+-----------------------------------------------------------+
| '*'             | Matches everything but the directory separator            |
+-----------------+-----------------------------------------------------------+
| '**'            | Matches everything.                                       |
+-----------------+-----------------------------------------------------------+
```