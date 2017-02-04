```
$ echo "1+1" > add.r
$ coala --files add.r --bears FormatRBear
Executing section Default...

add.r
|   1| 1+1
|    | [NORMAL] FormatRBear:
|    | Inconsistency found.
|----|    | /home/lasse/prog/coala/landing-frontend/add.r
|    |++++| /home/lasse/prog/coala/landing-frontend/add.r
|   1|    |-1+1
|    |   1|+1 + 1
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Apply patch
|    |  3: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
