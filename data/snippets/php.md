```
$ echo "<?php echo '<p>Hello World</p>'; ?" >> test.php
$ coala --files test.php --bears PHPLintBear
Executing section Default...

test.php
|   1| <?php·echo·'<p>Hello·World</p>';·?
|    | [MAJOR] PHPLintBear:
|    | syntax error, unexpected '?', expecting end of file
|    | *0: Do nothing
|    |  1: Open file(s)
|    |  2: Add ignore comment
|    | Enter number (Ctrl-D to exit):
1 $
```
