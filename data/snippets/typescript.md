```
$ echo "class Something {constructor(public something: string){}}" >> test.ts
$ coala --files test.ts --bears TSLintBear
Executing section Default...

test.ts
|   1| class·Something·{constructor(public·something:·string){}}
|    | [NORMAL] TSLintBear (one-line):
|    | missing whitespace
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):
```
