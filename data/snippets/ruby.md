```
$ echo 'puts ( "Hello World" )' > hello.rb
$ coala --files hello.rb --bears RubocopBear
Executing section Default...

hello-world.rb
|   1| puts·(·"Hello·world!"·)
|    | [INFO] RuboCopBear (Style/FileName):
|    | The name of this source file (`hello-world.rb`) should use snake_case.
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):

hello-world.rb
|   1| puts·(·"Hello·world!"·)
|    | [NORMAL] RuboCopBear (Lint/ParenthesesAsGroupedExpression):
|    | `(...)` interpreted as grouped expression.
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):

hello-world.rb
|   1| puts·(·"Hello·world!"·)
|    | [INFO] RuboCopBear (Style/RedundantParentheses):
|    | Don't use parentheses around a literal.
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):

hello-world.rb
|   1| puts·(·"Hello·world!"·)
|    | [INFO] RuboCopBear (Style/StringLiterals):
|    | Prefer single-quoted strings when you don't need string interpolation or special symbols.
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):

hello-world.rb
|   1| puts·(·"Hello·world!"·)
|    | [INFO] RuboCopBear (Style/SpaceInsideParens):
|    | Space inside parentheses detected.
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
