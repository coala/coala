```
$ echo "int add ( a , b ) { return a + b; }" >> test.c
$ coala --files test.c --bears GNUIndentBear
Executing section Default...

test.c
|   1| int•add•(•a•,•b•)•{•return•a•+•b;•}
|    | [NORMAL] GNUIndentBear:
|    | Indentation can be improved.
|    | +5 -1 in /home/lasse/prog/coala/landing-frontend/test.c
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Apply patch
|    |  3: Show patch
|    |  4: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
