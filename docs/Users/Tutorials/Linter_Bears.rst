Linter Bears
============

Welcome. This tutorial aims to show you how to use the Lint
class in order to integrate linters in your bears.

Why is This Useful?
-------------------

A lot of programming languages already have linters implemented, so if your
project uses a language that does not already have a linter Bear you might
need to implement it on your own. Don't worry, it's easy!

What do we Need?
----------------

First of all, we need the linter that we are going to use.
In this tutorial we will build the HTMLTutorialBear so we need an html
linter.
`This <https://github.com/deezer/html-linter>`__ one will do.
Since it is a python package we can go ahead and install it with

::

    $ pip install html-linter

Writing the Bear
----------------

Since we are going to use the Lint class we should go ahead and
import it together with LocalBear (all bears that handle only one file
inherit from LocalBear). Also we will go ahead and write the class
head. It should inherit both LocalBear and Lint.

::

    from coalib.bearlib.abstractions.Lint import Lint
    from coalib.bears.LocalBear import LocalBear

    class HTMLTutorialBear(LocalBear, Lint):

To make our bear use a linter we will have to overwrite some of the
predefined values of the Lint class. Some of the most important are
``executable`` and ``output_regex``.

We use ``executable`` to specify the linter executable. In our case it would
be

::

    executable = 'html_lint.py'

The ``output_regex`` is used to group parts of the output (such as ``lines``,
``columns``, ``severity`` and ``message``) so it can be used by the Lint
class to yield Results (more on communicating with the user
:doc:`Writing Bears <Writing_Bears>`).

In order to figure out the ``output_regex`` we have to first see how the
linter output looks. I will use this file as ``sample.html``

::

    <html>
      <body>
        <h1>Hello, world!</h1>
      </body>
    </html>

Now we can run

.. Start ignoring LineLengthBear

::

    $ html_lint.py sample.html
    1:1: Info: Optional Tags: Omit optional tags (optional): You may remove the opening "html" tag.
    2:3: Info: Optional Tags: Omit optional tags (optional): You may remove the opening "body" tag.
    4:3: Info: Optional Tags: Omit optional tags (optional): You may remove the closing "body" tag.
    5:1: Info: Optional Tags: Omit optional tags (optional): You may remove the closing "html" tag.

.. Stop ignoring LineLengthBear

Our ``output_regex`` should look like this

::

    (line):(column): (severity): (message)

Or in `python regex <https://docs.python.org/3/library/re.html>`__

.. Start ignoring LineLengthBear

::

    (?P<line>\d+):(?P<column>\d+):\s(?P<severity>Error|Warning|Info):\s(?P<message>.+)

.. Stop ignoring LineLengthBear

Now that we found out our ``output_regex`` (we might want to test it just
to be sure, https://regex101.com/#python is a great tool for this purpose).
We can now compile and add our regex using the ``re`` python library like so
(the regex was split into 2 lines to focus on readability)

::

    import re

    from coalib.bearlib.abstractions.Lint import Lint
    from coalib.bears.LocalBear import LocalBear


    class HTMLTutorialBear(LocalBear, Lint):
        executable = 'html_lint.py'
        output_regex = re.compile(
            r'(?P<line>\d+):(?P<column>\d+):\s'
            r'(?P<severity>Error|Warning|Info):\s(?P<message>.+)'
        )

*coala* uses three types of severities

-  INFO
-  NORMAL
-  MAJOR

which are defined in ``coalib.results.RESULT_SEVERITY``. In order to use
the severity group from the regex we will first have to map the output
severities (as seen in the linter and as used in the regex above
``Info``, ``Warning``, ``Error``) to the defined *coala* severities
(above stated ``INFO``, ``NORMAL``, ``MAJOR``).

Luckily for us the Lint class provides us with the ``severity_map``
property. ``severity_map`` is just a dictionary of strings that
should be mapped to the define *coala* severities. Let's go ahead and import
``coalib.results.RESULT_SEVERITY`` and write our ``severity_map``. Our code
could look like this

::

    import re

    from coalib.bearlib.abstractions.Lint import Lint
    from coalib.bears.LocalBear import LocalBear
    from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


    class HTMLTutorialBear(LocalBear, Lint):
        executable = 'html_lint.py'
        output_regex = re.compile(
            r'(?P<line>\d+):(?P<column>\d+):\s'
            r'(?P<severity>Error|Warning|Info):\s(?P<message>.+)'
        )
        severity_map = {
            "Info": RESULT_SEVERITY.INFO,
            "Warning": RESULT_SEVERITY.NORMAL,
            "Error": RESULT_SEVERITY.MAJOR
        }

As with every other bear (see :doc:`Writing Bears <Writing_Bears>`) we have
to define our run method.

::

    def run(self, filename, file):

        return self.lint(filename)

And that should be enough. The lint() method of the Lint class will do the
rest for us.

We can test our bear like this

::

    $ coala --bear-dirs=. --bears=HTMLTutorialBear --files=sample.html

.. note::

    In order for the above command to work we should have 2 files in
    our current dir: ``HTMLTutorialBear.py`` and our ``sample.html``.
    Naming is **very** important in *coala*. *coala* will look for bears
    by their **filename** and display them based on their
    **classname**.

Adding Settings to our Bear
---------------------------

If we run

::

    $ html_lint.py -h

We can see that there is a ``--disable`` option which lets us disable some
checks. Let's add that functionality to our bear.

First of all we have to import the setting that we are going to use from
coalib. Since ``--disable`` needs a comma separated list we can use a list
to keep our options. For that we will import ``typed_list`` like so

::

    from coalib.settings.Setting import typed_list

``typed_list(item_type)`` is a function that converts the given input
(which the user will pass to the Bear as a setting) into a list of
items and afterwards will apply a conversion to type ``item_type`` to each
item in the list (you can also use basic types like ``int``, ``bool``, etc.
see :doc:`Writing Bears <Writing_Bears>`)
Next, we have to add our setting as a parameter for the ``run()`` method
of our bear.
We will give the param a sugestive name like ``htmllint_ignore``.

::

    def run(self,
            filename,
            file,
            htmllint_ignore: typed_list(str)=[]):
        '''
        Checks the code with `html_lint.py` on each file separately.

        :param htmllint_ignore: List of checkers to ignore.
        '''

.. note::

    The documentation of the param is parsed by *coala* and it will be used
    as help to the user for that specific setting.

The last thing we need to do is join the strings in the ``html_ignore``,
append them to ``--disable=`` and add it as an argument. There are alot
of ways of doing that.

::

    ignore = ','.join(part.strip() for part in htmllint_ignore)
    self.arguments = '--disable=' + ignore
    return self.lint(filename)

Right place for '{filename}'
----------------------------

Depending on where the executable (``html_lint.py`` in this case) wants the
file-name (eg. ``sample.html``) to be present in the command which does the
linting, we add ``'{filename}'`` to the arguments. When we run
``html_lint.py -h``, we can see that the command signature is:
``html5_lint.py [--disable=DISABLE] FILENAME...``

So, we want ``'{filename}'`` at the end of the arguments.

::

    self.arguments = '--disable=' + ignore
    self.arguments += ' {filename}'
    return self.lint(filename)


Finished Bear
-------------

Well done, you made it this far! Now you should have built a fully
functional HTML Lint Bear. If you followed the code from this tutorial
it should look something like this

::

    import re

    from coalib.bearlib.abstractions.Lint import Lint
    from coalib.bears.LocalBear import LocalBear
    from coalib.settings.Setting import typed_list
    from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


    class HTMLTutorialBear(LocalBear, Lint):
        executable = 'html_lint.py'
        output_regex = re.compile(
            r'(?P<line>\d+):(?P<column>\d+):\s'
            r'(?P<severity>Error|Warning|Info):\s(?P<message>.+)'
        )
        severity_map = {
            "Info": RESULT_SEVERITY.INFO,
            "Warning": RESULT_SEVERITY.NORMAL,
            "Error": RESULT_SEVERITY.MAJOR
        }

        def run(self,
                filename,
                file,
                htmllint_ignore: typed_list(str)=[]):
            '''
            Checks the code with `html_lint.py` on each file separately.

            :param htmllint_ignore: List of checkers to ignore.
            '''
            ignore = ','.join(part.strip() for part in htmllint_ignore)
            self.arguments = '--disable=' + ignore
            self.arguments += ' {filename}'
            return self.lint(filename)

Running and Testing our Bear
----------------------------

By running

::

    $ coala --bear-dirs=. --bears=HTMLTutorialBear -B

We can see that our Bear setting is documented properly. To use *coala*
with our Bear on `sample.html` we run

::

    $ coala --bear-dirs=. --bears=HTMLTutorialBear --files=sample.html

To use our `htmllint_ignore` setting we can do

::

    $ coala --bear-dirs=. --bears=HTMLTutorialBear \
    > -S htmllint_ignore=optional_tag --files=sample.html

This will not output anything because all the messages had the
`optional_tag`.

You now know how to write a linter Bear and also how to use it in your
project.
Congratulations!
