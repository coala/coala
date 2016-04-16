Codestyle for coala
===================

*coala* follows the `PEP8
codestyle <https://www.python.org/dev/peps/pep-0008/>`__ with a maximum
line length of 80 characters including newline. Invoke ``coala`` to let
it correct your code automatically.

Additional Style Guidelines
---------------------------

Documentation Comments
~~~~~~~~~~~~~~~~~~~~~~

A documentation comment consists of 2 parts - the description of what
the function/class/module does followed by the parameters it takes in,
the return value it gives out and the exceptions it can raise.

Nothing should be written on the first and last line where the docstring
begins and ends, and a newline should separate the description and the
rest. Each message in the documentation comment must end with a
full-stop. Also the description of all arguments and the return value
should begin at the same column.

Example:

::

    def area(length, breadth):
        """
        Finds the area of a rectangle of the given length and breadth.

        :param length:      The length of the rectangle.
        :param breadth:     The breadth of the rectangle.
        :return:            The area of the rectangle.
        :raises ValueError: Raises ValueError if the arguments are not of type
                            float or int.
        """

If the description for a param or other keywords exceeds 1 line,
continue it in the next. Make sure that the second line is aligned Below
the first line.

Example :

::

    :param something: A very long line describing the variable something
                      in great detail.
    :return:          This message also started in the same column and it
                      starts again at the same column as the rest of the
                      messages.

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

This will raise a ``TypeError`` if ``a``, ``b`` or ``c`` are no strings
and ``c`` is not ``None``.
