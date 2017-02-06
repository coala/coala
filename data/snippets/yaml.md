```
$ echo "---
dict :
  key:
        value
" >> test.yaml
$ coala --files test.yaml --bears YAMLLintBear
Executing section Default...

test.yaml
|   2| dict·:
|    | [MAJOR] YAMLLintBear:
|    | too many spaces before colon (colons)
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):

test.yaml
|   4| ········value
|    | [MAJOR] YAMLLintBear:
|    | wrong indentation: expected 4 but found 8 (indentation)
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
