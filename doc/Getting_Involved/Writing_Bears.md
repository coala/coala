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
        self.debug("Hello World! Checking file", filename, ".")
```

This bear is stored at `./bears/HelloWorldBear`

In order to let coala execute this bear you need to let coala know where to
find it. We can do that with the `-d` (`--bear-dirs`) argument:

`coala -f src/*.c -d bears -b HelloWorldBear -L DEBUG`

You should now see the debug message for our sample file.

The Bear class also supports `warn` and `err`.

## Communicating with the User

Now we can send messages through the queue, we can do the real work. Lets say:

 * We want some information from the user (e.g. the tab width if we rely on
   indentation)
 * We've got some useful information for the user and want to show it to him.
   This might be some issue with his code or just an information like the
   number of lines.

So let's extend our HelloWorldBear a bit, I've named the new bear with the
creative name CommunicationBear:

```python
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result


class CommunicationBear(LocalBear):
    def run(self,
            filename,
            file,
            user_input: str):
        """
        Communicates with the user.

        :param user_input: Arbitrary user input.
        """
        self.debug("Got '{ui}' as user input of type {type}.".format(
            ui=user_input,
            type=type(user_input)))

        return [Result(message="A hello world result.",
                       origin=self,
                       file=filename)]
```

Try executing it:

```
coala -f src/*.c -d bears -b CommunicationBear -L DEBUG
```

Hey, we'll get asked for the user_input! Wasn't that easy? Go ahead, enter
something and observe the output.

So, what did coala do here?

First, coala looked at the parameters of the run method and found that we
need some value named user_input. Then it parsed our documentation comment and
found a description for the parameter which was shown to us to help us choose
the right value. After the needed values are provided, coala converts us the
value into a string because we've provided the `str` annotation for this
parameter. If no annotation is given or the value isn't convertible into the
desired data type, you will get a `coalib.settings.Setting.Setting`.

### What Data Types are Supported?

The Setting does support some very basic types:

 * String (`str`)
 * List of strings (`list`, values will be split by comma)
 * Boolean (`bool`, will accept values like `true`, `yes`, `yeah`, `no`,
   `nope`, `false`)

If you need another type, you can write the conversion function yourself and
use this function as the annotation. We've provided e.g.:

 * `coalib.settings.Setting.path`, converts to an absolute file path relative
   to the file/command where the setting was set
 * `coalib.settings.Setting.path_list`, converts to a list of absolute file
   paths relative to the file/command where the setting was set

# Results

In the end we've got a result. If a file is provided, coala will show the file,
if a line is provided, coala will also show a few lines before the affecting
line. There are a few result types so you can e.g. create a PatchResult that
proposes a code change to the user. If the user likes it, coala will apply it
automatically - you don't need to care.
