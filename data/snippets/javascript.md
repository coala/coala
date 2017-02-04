```
$ echo "function multiply(a, b) { return a*c; }" >> mult.js
$ coala --files mult.js --bears ESLintBear
Executing section Default...

mult.js
|   1| function•multiply(a,•b)•{•return•a*c;•}
|    | [MAJOR] ESLintBear (no-undef):
|    | 'c' is not defined.
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):

mult.js
|   1| function•multiply(a,•b)•{•return•a*c;•}
|    | [MAJOR] ESLintBear (no-unused-vars):
|    | 'b' is defined but never used
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):

mult.js
|   1| function•multiply(a,•b)•{•return•a*c;•}
|    | [MAJOR] ESLintBear (no-unused-vars):
|    | 'multiply' is defined but never used
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
