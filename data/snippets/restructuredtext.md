```
$ echo "=====
Hello World
===========

Hi there."> test.rst
$ coala --files test.rst --bears reSTLintBear
Executing section Default...

test.rst
|   1| =====
|    | [MAJOR] reSTLintBear:
|    | Title overline & underline mismatch.
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Print debug message
|    |  3: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
