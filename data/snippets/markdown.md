```
$ echo "Some Heading
-----
" > test.md
$ coala --files test.md --bears MarkdownBear
Executing section Default...

test.md
|   1| Some•Heading
|   2| -----
|   3|
|    | [NORMAL] MarkdownBear:
|    | The text does not comply to the set style.
|----|    | /home/lasse/prog/coala/landing-frontend/test.md
|    |++++| /home/lasse/prog/coala/landing-frontend/test.md
|   1|    |-Some Heading
|----|    | --
|   2|    |-
|    |   1|+## Some Heading
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Apply patch
|    |  3: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
