```
$ echo "<button class="btn btn-default">Is this correct Bootstrap markup, Bootlint?</button>" >> booty.html
$ coala --files booty.html --bears BootLintBear
Executing section Default...

booty.html
|   1| <button•class=btn•btn-default>Is•this•correct•Bootstrap•markup,•Bootlint?</button>
|    | [NORMAL] BootLintBear:
|    | Found one or more `<button>`s missing a `type` attribute.
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
1 $
```
