```
$ echo ".someclass { height: 10px; height: 10px; }" >> test.css
$ coala --files test.css --bears CSSLintBear
Executing section Default...

test.css
|   1| .someclass•{•height:•10px;•height:•10px;•}
|    | [NORMAL] CSSLintBear:
|    | Duplicate property 'height' found. (duplicate-properties)
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
