Codestyle for coala
=====================

coala follows the
`PEP8 codestyle <https://www.python.org/dev/peps/pep-0008/>`__ with a maximum
line length of 80 characters including newline. Invoke ``coala`` to let
it correct your code automatically.

Additional Style Guidelines
---------------------------

Documentation Comments
~~~~~~~~~~~~~~~~~~~~~~

A documentation comment consists of 2 parts split by a newline:

- the description of what it does
- a list of the parameters it takes in and their descriptions, the return
  value it gives out and the exceptions it may raise

Nothing should be written on the first and last line where the docstring
begins and ends, and each message in the documentation comment must end with a
full-stop. Also, the description of all arguments, return value and errors
raised shall be on a newline, indented by 4 spaces.

Example:

::

    def area(length, breadth):
        """
        Finds the area of a rectangle of the given length and breadth.

        :param length:
            The length of the rectangle.
        :param breadth:
            The breadth of the rectangle.
        :return:
            The area of the rectangle.
        :raises ValueError:
            Raises ValueError if the arguments are not of type
            ``float`` or ``int``.
        """

If the description for a param or other keywords exceeds 1 line,
continue it in the next. Make sure that the second line is aligned below
the first line.

Type Checking
~~~~~~~~~~~~~

If you want to assure that parameters have a certain type, you can use
the ``enforce_signature`` decorator and simply annotate your function
with the allowed types:

.. code:: python

    @enforce_signature
    def concatenate_strings(a: str, b: str, c: (str, None)=None):
        if c is None:
            c = ""
        return a + b + c

This will raise a ``TypeError`` if ``a``, ``b`` or ``c`` are not strings
and ``c`` is not ``None``.

Line Continuation
~~~~~~~~~~~~~~~~~

Since line continuation is not covered by PEP8 coding style guide you are
supposed to keep your multiple-line lists, dicts, tuples, function definitions,
function calls, and any such structures either:

- stay on one line
- span multiple lines that list one parameter/item each
