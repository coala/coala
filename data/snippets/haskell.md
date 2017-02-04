```
$ echo "putStrLn (\"Hello World\")" > hello.hs
$ coala --files hello.hs --bears HaskellLintBear
Executing section Default...

hello.hs
|   1| putStrLn•("Hello•World")
|    | [NORMAL] HaskellLintBear:
|    | Redundant bracket
|----|    | /home/lasse/prog/coala/landing-frontend/hello.hs
|    |++++| /home/lasse/prog/coala/landing-frontend/hello.hs
|   1|    |-putStrLn ("Hello World")
|    |   1|+putStrLn "Hello World"
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Apply patch
|    |  3: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
