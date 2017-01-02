Linter Bears
============

Welcome. This tutorial aims to show you how to use the ``@linter`` decorator in
order to integrate linters in your bears.

.. note::

  If you are planning to create a bear that does static code analysis without
  wrapping a tool, please refer to :doc:`this link instead<Writing_Bears>`.

Why is This Useful?
-------------------

A lot of programming languages already have linters implemented, so if your
project uses a language that does not already have a linter Bear you might
need to implement it on your own. Don't worry, it's easy!

What do we Need?
----------------

First of all, we need the linter executable that we are going to use.
In this tutorial we will build the PylintTutorialBear so we need Pylint, a
common linter for Python. It can be found `here <https://www.pylint.org/>`__.
Since it is a python package we can go ahead and install it with

::

    $ pip3 install pylint

Writing the Bear
----------------

To write a linter bear, we need to create a class that interfaces with our
linter-bear infrastructure, which is provided via the ``@linter`` decorator.

::

    from coalib.bearlib.abstractions.Linter import linter

    @linter(executable='pylint')
    class PylintTutorialBear:
        pass

As you can see ``pylint`` is already provided as an executable name which gets
invoked on the files you are going to lint. This is a mandatory argument for
the decorator.

The linter class is only capable of processing one file at a time, for this
purpose ``pylint`` or the external tool needs to be invoked every time with the
appropriate parameters. This is done inside ``create_arguments``,

::

    @linter(executable='pylint')
    class PylintTutorialBear:
        @staticmethod
        def create_arguments(filename, file, config_file):
            pass

``create_arguments`` accepts three parameters:

- ``filename``: The absolute path to the file that gets processed.
- ``file``: The contents of the file to process, given as a list of lines
  (including the return character).
- ``config_file``: The absolute path to a config file to use. If no config file
  is used, this parameter is ``None``. More on that later.

You can use these parameters to construct the command line arguments. The
linter expects from you to return an argument sequence here. A tuple is
preferred. We will do this soon for ``PylintTutorialBear``.

.. note::

    ``create_arguments`` doesn't have to be a static method. In this case you
    also need to prepend ``self`` to the parameters in the signature. Some
    functionality of ``@linter`` is only available inside an instance, like
    logging.

    ::

        def create_arguments(self, filename, file, config_file):
            self.log("Hello world")

So which are the exact command line arguments we need to provide? It depends on
the output format of the linter. The ``@linter`` decorator is capable of
handling different output formats:

- ``regex``: This parses issue messages yielded by the underlying executable.
- ``corrected``: Auto-generates results from a fixed/corrected file provided by
  the tool.

In this tutorial we are going to use the ``regex`` output format. But before we
continue with modifying our bear, we need to figure out how exactly output from
Pylint looks like so we can parse it accordingly.

We get some promising output when invoking Pylint with

::

    $ pylint --msg-template="L{line}C{column}: {msg_id} - {msg}" --reports=n

Sample output looks like this:

::

    No config file found, using default configuration
    ************* Module coalib.bearlib.abstractions.Linter
    L1C0: C0111 - Missing module docstring
    L42C48: E1101 - Class 'Enum' has no 'reverse' member
    L77C32: E1101 - Class 'Enum' has no 'reverse' member
    L21C0: R0912 - Too many branches (16/12)
    L121C28: W0613 - Unused argument 'filename'

This is something we can parse easily with a regex. So let's implement
everything we've found out so far:

::

    @linter(executable='pylint',
            output_format='regex',
            output_regex=r'L(?P<line>\d+)C(?P<column>\d+): (?P<message>.*)')
    class PylintTutorialBear:
        @staticmethod
        def create_arguments(filename, file, config_file):
            return ('--msg-template="L{line}C{column}: {msg_id} - {msg}"',
                    '--reports=n', filename)

As you can see, the ``output_regex`` parameter consists of named groups. These
are important to construct a meaningful result that contains the information
that is printed out.

For the exact list of named groups ``@linter`` recognizes, see the `API
documentation <https://api.coala.io/en/latest/>`_.

For more info generally on regexes, see `Python re module
<https://docs.python.org/3/library/re.html>`_.

Let's brush up our ``output_regex`` a bit to use even more information:

::

    @linter(...
            output_regex=r'L(?P<line>\d+)C(?P<column>\d+): '
                         r'(?P<message>(?P<origin>.\d+) - .*)'),
            ...)

Now we use the issue identification as the origin so we are able to deactivate
single rules via ignore statements inside code.

This class is already fully functional and allows to parse issues yielded by
Pylint!

Using Severities
----------------

coala uses three types of severities that categorize the importance of a
result:

-  INFO
-  NORMAL
-  MAJOR

which are defined in ``coalib.results.RESULT_SEVERITY``. Pylint output contains
severity information we can use:

::

    L1C0: C0111 - Missing module docstring

The letter before the error code is the severity. In order to make use of the
severity, we need to define it inside the ``output_regex`` parameter using the
named group ``severity``:

::

    @linter(...
            output_regex=r'L(?P<line>\d+)C(?P<column>\d+): (?P<message>'
                         r'(?P<origin>(?P<severity>[WFECRI])\d+) - .*)',
            ...)

So we want to take up the severities denoted by the letters ``W``, ``F``,
``E``, ``C``, ``R`` or ``I``. In order to use this severity value, we will
first have to provide a map that takes the matched severity letter and maps it
to a severity value of ``coalib.results.RESULT_SEVERITY`` so coala
understands it. This is possible via the ``severity_map`` parameter of
``@linter``:

::

    from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY

    @linter(...
            severity_map={'W': RESULT_SEVERITY.NORMAL,
                          'F': RESULT_SEVERITY.MAJOR,
                          'E': RESULT_SEVERITY.MAJOR,
                          'C': RESULT_SEVERITY.NORMAL,
                          'R': RESULT_SEVERITY.NORMAL,
                          'I': RESULT_SEVERITY.INFO},
            ...)

``coalib.results.RESULT_SEVERITY`` contains three different values, ``Info``,
``Warning`` and ``Error`` you can use.

We can test our bear like this

::

    $ coala --bear-dirs=. --bears=PylintTutorialBear --files=sample.py

.. note::

    In order for the above command to work we should have 2 files in
    our current dir: ``PylintTutorialBear.py`` and our ``sample.py``.
    Naming is **very** important in coala. coala will look for bears
    by their **filename** and display them based on their
    **classname**.

Normally, providing a severity-map is not needed, as coala has a default
severity-map which recognizes many common words used for severities. Check out
the API documentation for keywords supported!

Suggest Corrections Using the ``corrected`` Output Format
---------------------------------------------------------

This output format is very simple to use and doesn't require further setup from
your side inside the bear:

::

    @linter(...
            output_format='corrected')

If your underlying tool generates a corrected file, the class automatically
generates patches for the changes made and yields results accordingly.

Adding Settings to our Bear
---------------------------

If we run

::

    $ pylint --help

We can see that there is a ``--rcfile`` option which lets us specify a
configuration file for Pylint. Let's add that functionality to our bear.

::

    import os

    from coalib.bearlib.abstractions.Linter import linter
    from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY

    @linter(executable='pylint',
            output_format='regex',
            output_regex=r'L(?P<line>\d+)C(?P<column>\d+): '
                         r'(?P<message>(?P<severity>[WFECRI]).*)',
            severity_map={'W': RESULT_SEVERITY.NORMAL,
                          'F': RESULT_SEVERITY.MAJOR,
                          'E': RESULT_SEVERITY.MAJOR,
                          'C': RESULT_SEVERITY.NORMAL,
                          'R': RESULT_SEVERITY.NORMAL,
                          'I': RESULT_SEVERITY.INFO})
    class PylintTutorialBear:
        @staticmethod
        def create_arguments(filename, file, config_file,
                             pylint_rcfile: str=os.devnull):
            return ('--msg-template="L{line}C{column}: {msg_id} - {msg}"',
                    '--reports=n', '--rcfile=' + pylint_rcfile, filename)

Just adding the needed parameter to the ``create_arguments`` signature
suffices, like you would do for other bears inside ``run``! Additional
parameters are automatically queried from the coafile. Let's also add some
documentation together with the metadata attributes:

::

    @linter(...)
    class PylintTutorialBear:
        """
        Lints your Python files!

        Check for codings standards (like well-formed variable names), detects
        semantical errors (like true implementation of declared interfaces or
        membership via type inference), duplicated code.

        See http://pylint-messages.wikidot.com/all-messages for a list of all
        checks and error codes.
        """

        @staticmethod
        def create_arguments(filename, file, config_file,
                             pylint_rcfile: str=os.devnull):
            """
            :param pylint_rcfile:
                The configuration file Pylint shall use.
            """
            ...

.. note::

    The documentation of the param is parsed by coala and it will be used
    as help to the user for that specific setting.

Finished Bear
-------------

Well done, you made it this far! Now you should have built a fully
functional Python linter Bear. If you followed the code from this tutorial
it should look something like this

::

    import os

    from coalib.bearlib.abstractions.Linter import linter
    from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY

    @linter(executable='pylint',
            output_format='regex',
            output_regex=r'L(?P<line>\d+)C(?P<column>\d+): '
                         r'(?P<message>(?P<severity>[WFECRI]).*)',
            severity_map={'W': RESULT_SEVERITY.NORMAL,
                          'F': RESULT_SEVERITY.MAJOR,
                          'E': RESULT_SEVERITY.MAJOR,
                          'C': RESULT_SEVERITY.NORMAL,
                          'R': RESULT_SEVERITY.NORMAL,
                          'I': RESULT_SEVERITY.INFO})
    class PylintTutorialBear:
        """
        Lints your Python files!

        Check for codings standards (like well-formed variable names), detects
        semantical errors (like true implementation of declared interfaces or
        membership via type inference), duplicated code.

        See http://pylint-messages.wikidot.com/all-messages for a list of all
        checks and error codes.

        https://pylint.org/
        """

        @staticmethod
        def create_arguments(filename, file, config_file,
                             pylint_rcfile: str=os.devnull):
            """
            :param pylint_rcfile:
                The configuration file Pylint shall use.
            """
            return ('--msg-template="L{line}C{column}: {msg_id} - {msg}"',
                    '--reports=n', '--rcfile=' + pylint_rcfile, filename)

Adding Metadata Attributes
--------------------------

Now we need to add some more precious information to our bear. This helps
by giving more information about each bear and also helps some functions
gather information by using these values. Our bear now looks like:

::

  import os

  from coalib.bearlib.abstractions.Linter import linter
  from dependency_management.requirements.PipRequirement import PipRequirement
  from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY

  @linter(executable='pylint',
          output_format='regex',
          output_regex=r'L(?P<line>\d+)C(?P<column>\d+): '
                       r'(?P<message>(?P<severity>[WFECRI]).*)',
          severity_map={'W': RESULT_SEVERITY.NORMAL,
                        'F': RESULT_SEVERITY.MAJOR,
                        'E': RESULT_SEVERITY.MAJOR,
                        'C': RESULT_SEVERITY.NORMAL,
                        'R': RESULT_SEVERITY.NORMAL,
                        'I': RESULT_SEVERITY.INFO})
  class PylintTutorialBear:
      """
      Lints your Python files!

      Check for codings standards (like well-formed variable names), detects
      semantical errors (like true implementation of declared interfaces or
      membership via type inference), duplicated code.

      See http://pylint-messages.wikidot.com/all-messages for a list of all
      checks and error codes.

      https://pylint.org/
      """

      LANGUAGES = {"Python", "Python 2", "Python 3"}
      REQUIREMENTS = {PipRequirement('pylint', '1.*')}
      AUTHORS = {'The coala developers'}
      AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
      LICENSE = 'AGPL-3.0'
      CAN_DETECT = {'Unused Code', 'Formatting', 'Duplication', 'Security',
                    'Syntax'}

      @staticmethod
      def create_arguments(filename, file, config_file,
                           pylint_rcfile: str=os.devnull):
        """
        :param pylint_rcfile:
            The configuration file Pylint shall use.
        """
        return ('--msg-template="L{line}C{column}: {msg_id} - {msg}"',
                '--reports=n', '--rcfile=' + pylint_rcfile, filename)

Running and Testing our Bear
----------------------------

By running

::

    $ coala --bear-dirs=. --bears=PylintTutorialBear -B

We can see that our Bear setting is documented properly. To use coala
with our Bear on `sample.py` we run

::

    $ coala --bear-dirs=. --bears=PylintTutorialBear --files=sample.py

To use our `pylint_rcfile` setting we can do

::

    $ coala --bear-dirs=. --bears=PythonTutorialBear \
    > -S rcfile=my_rcfile --files=sample.py

You now know how to write a linter Bear and also how to use it in your
project.

Congratulations!

Where to Find More...
---------------------

If you need more information about the ``@linter`` decorator, refer to the API
documentation.
