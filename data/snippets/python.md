```
$ echo "import os

print( 'Hello World' )
" > hello.py
$ coala --files hello.py --bears PEP8Bear,PyUnusedCodeBear
Executing section Default...

hello.py
|   1| import•os
|    | [NORMAL] PyUnusedCodeBear:
|    | This file contains unused source code.
|----|    | /home/user/hello/hello.py
|    |++++| /home/user/hello/hello.py
|   1|    |-import os
|   2|   1|
|   3|   2| print( 'Hello World' )
|   4|   3|
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Apply patch
|    |  3: Add ignore comment
|    | Enter number (Ctrl-D to exit): <ENTER>

hello.py
|   3| print(•'Hello•World'•)
|   4|
|    | [NORMAL] PEP8Bear:
|    | The code does not comply to PEP8.
|----|    | /home/user/hello/hello.py
|    |++++| /home/user/hello/hello.py
|   1|   1| import os
|   2|   2|
|   3|    |-print( 'Hello World' )
|   4|    |-
|    |   3|+print('Hello World')
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Apply patch
|    |  3: Add ignore comment
|    | Enter number (Ctrl-D to exit): <ENTER>
1 $
```