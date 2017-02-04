```
$ echo "{ \"value\": 5 }" >> test.json
$ coala --files test.json --bears JSONFormatBear
Executing section Default...

test.json
|   1| {•"value":•5•}
|    | [NORMAL] JSONFormatBear:
|    | This file can be reformatted by sorting keys and following indentation.
|----|    | /home/lasse/prog/coala/landing-frontend/test.json
|    |++++| /home/lasse/prog/coala/landing-frontend/test.json
|   1|    |-{ "value": 5 }
|    |   1|+{
|    |   2|+    "value": 5
|    |   3|+}
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Apply patch
|    |  3: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
