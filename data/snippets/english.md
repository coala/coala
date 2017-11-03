```
$ echo "This will faciliate review by other developers, very important if you want your patch accepted." > test.english
$ coala --files test.english --bears ProseLintBear
Executing section Default...

test.english
|   1| This·will·faciliate·review·by·other·developers,·very·important·if·you·want·your·patch·accepted.
|    | [NORMAL] ProseLintBear:
|    | Substitute 'damn' every time you're inclined to write 'very;' your editor will delete it and the writing will be just as it should be.
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
