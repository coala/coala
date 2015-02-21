# Guide to Write a Bear

Welcome. This document presents information on how to write a bear for coala.
It assumes you know how to use coala. If not please read our main tutorial!

The sample sources for this tutorial lie at our coala-tutorial repository, go
clone it with:

```
git clone https://github.com/coala-analyzer/coala-tutorial.git
```

All paths and commands given here are meant to be executed from the root
directory of the coala-tutorial repository.

## What is a bear?

A bear is meant to do some analysis on source code. The source code will
provided by coala so the bear doesn't have to care where it comes from or where
it goes.

A bear can communicate with the user via two ways:

 * Via log messages
 * Via results

Log messages will be logged according to the users settings and are usually
used if something goes wrong. However you can use debug for providing
development related debug information since it will not be shown to the user by
default. If error/failure messages are used, the bear is expected not to
continue analysis.

## A Hello World Bear

Below is the code given for a simple bear that sends a debug message for each
file:

```python
from coalib.bears.LocalBear import LocalBear


class HelloWorldBear(LocalBear):
    def run(self,
            filename,
            file):
        self.debug_msg("Hello World! Checking file", filename, ".")
```

This bear is stored at `./bears/HelloWorldBear`

In order to let coala execute this bear you need to let coala know where to
find it. We can do that with the `-d` (`--bear-dirs`) argument:

`coala -f src/*.c -d bears -b HelloWorldBear -L DEBUG`

You should now see the debug message for our sample file.
