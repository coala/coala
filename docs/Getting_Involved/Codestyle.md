# Codestyle for coala

Please note that these guidelines are currently work in progress. They will be
extended soon.

# Introduction

The main programming language for coala is python 3. This document specifies
how python code should look to ensure maximum readability and consistency. It
is mainly derived from the
[PEP8 style guide](https://www.python.org/dev/peps/pep-0008/)
and thus merely specifies visual aspects of the code.

The rules given here are mandatory to ensure consistency. It is encouraged
to only violate the style guide if this increases readability and clarity.
If this is the case, a reason must be provided in a comment preceding the
affecting statement(s).

If you think some of our specifications could be changed or others could be
added to increase readability, feel free to discuss the issue with us.

# Spacing

## Indentation

Code has to be indented with 4 spaces per indentation level. Tabs are not
allowed to ensure consistency on different editor configurations. Python 3
disallows mixing of tabs and spaces.

### Multiline Statements

If you want to write a construct with brackets and elements that does not fit
into one line, Pythons implicit line joining inside parentheses, brackets
and braces must be used instead of ugly backslashes as newline escapes.

There are two variants for multiline statements.

You can align each element with the one above:

```python
foo = long_function_name(var_one,
                         var_two,
                         var_three,
                         var_four)
```

You can align all (including the first one) arguments one
indentation level deeper relative to the indentation level of the _next_
statement; this is called hanging indent:

```python
foo = long_function_name(
    var_one,
    var_two,
    var_three,
    var_four)
```

or

```python
def long_function_name(
        var_one,
        var_two,
        var_three,
        var_four):
    if (
            var_one or
            var_two or
            var_three or
            var_four):
        do_something_great()
```

This can be used for very long (e.g. constant string) arguments. Note that the
use of the first variant is not recommended for if statements because the next
statement is aligned with the elements of the multiline statement. Both
variants greatly clarify where the statement begins and make multiple arguments
very easy to read while they can be used fully consistently for all kinds of
multiline statements.

Multiple elements in one line are only allowed for single line statements in
general. It is way easier to scan through the arguments if they are all
aligned at the same point.

## Trailing Whitespace

Trailing whitespaces are not allowed and are to be stripped off. If your
editor does not remove them automatically you can let coala do it for you.

## Newline Characters

We use the unix style newline character '\n'.

Your git installation should be already configured to commit only unix style
line endings (`\n`) instead of CRLF in case you are using windows.

## Blank Lines

Top level classes and functions are to be seperated by two blank lines between
them. Use one newline between methods in classes.

Use blank lines in functions to indicate logical sections. Blank lines make
programs beautiful, don't be ashamed to use them!

```python
"""
Documentation
"""


def top_level_function():
    pass


class top_level_class:
    def foo(self):
        pass

    def bar(self):
        pass
```

# Maximum Line Length

Every line of code may hold only up to 79 characters (excluding the newline
character `\n`).

# Source File Encoding

Please use UTF-8. Use only ASCII characters for your source code, more
"complex" characters are only allowed in strings and documentation. If your
name is based on another alphabet than the latin one, please provide a latin
translation wherever you write it.

# Imports

## Position

Import statements should always be at the top of the file, right after
docstrings. They should be on separate lines unless two or more
classes or modules get imported from the same source.

Imports should be grouped into standard library imports first (e.g.
`import os`) and imports from the coala library (e.g.
`from coalib.output import Interactor`). Both groups should be separated by a
blank line.

## Absolute Imports

Coala specific imports should be absolute and therefore independent of
the position of the current module. This makes modules more robust against
file and package movements and emphasizes their origin and structure.

Good example:

```python
from coalib.output.printer import EspeakPrinter
```

Bad example:

```python
from . import EspeakPrinter
```

## Importing Classes Directly

STILL IN DISCUSSION: It is encouraged to import classes from modules directly
as long as it does not cause local name clashes.

Wildcard imports (`from <module\> import *`) are not allowed as they make it
unclear which names are present in the namespace.

# Functions

## Documentation Comments

A documentation comment consists of 2 parts - the description of what the
function/class/module does followed by the parameters it takes in, the
return value it gives out and the exceptions it can raise.

Nothing should be written on the first and last line where the docstring
begins and ends, and a newline should separate the description and the rest.
Each message in the documentation comment must end with a full-stop. Also
the description of all arguments and the return value should begin at the
same column.

Example:
```
def area(height, breadth):
    """
    Finds the area of a rectangle of the given length and breadth.

    :param length:      The length of the rectangle.
    :param breadth:     The breadth of the rectangle.
    :return:            The area of the rectangle.
    :raises ValueError: Raises ValueError if the arguments are not of type
                        float or int.
    """

```

If the description for a param or other keywords exceeds 1 line, continue
it in the next. Make sure that the second line is aligned Below the first
line.

Example :
```
:param something: A very long line describing the variable something
                  in great detail.
:return:          This message also started in the same column and it
                  starts again at the same column as the rest of the messages.
```

## Arguments

Do not use mutable arguments for default arguments in functions as they get
initialized only the first time the function is parser and are reused every
time the function is called. Instead use immutable ones, like tuples
instead of lists. If it is required to use a mutable argument (like dict,
class objects, etc), declare the default value as `None` and use a
condition inside the function to set it to the mutable argument.

Example:

```
def func(arg=None):
    arg = {"key": "val"} or arg
```
