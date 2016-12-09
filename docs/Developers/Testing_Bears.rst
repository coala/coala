How to use LocalBearTestHelper to test your bears
=================================================

coala has an awesome testing framework to write tests for bears with ease.

You can use the following to test your bears:

- ``LocalBearTestHelper.check_validity``
- ``LocalBearTestHelper.check_results``
- ``verify_local_bears``

Understanding through examples
------------------------------

Let us understand how to write tests for ``TooManyLinesBear`` in ``some_dir``.
``TooManyLinesBear`` checks if a file has less than or equal to
``max_number_of_lines`` lines. ``max_number_of_lines`` by default is 10.

.. code::

    from coalib.results.Result import Result
    from coalib.bears.LocalBear import LocalBear


    class TooManyLinesBear(LocalBear):

        def run(file,
                filename,
                max_number_of_lines: int=10):
            """
            Detects if a file has more than "max_number_of_lines" lines

            :param max_number_of_lines    Maximum number of lines to be
                                          allowed for a file. Default is 10.
            """

            if(len(file)>max_number_of_lines):
                yield Result(self, "Too many lines")

**EXAMPLE 1** using ``verify_local_bear``

.. code::

    from bears.some_dir.TooManyLinesBear import TooManyLinesBear
    from coalib.testing.LocalBearTestHelper import verify_local_bear

    good_file = '1\n2\n3\n4\n'.splitlines()
    bad_file = '1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n'.splitlines()

    TooManyLinesBearTest = verify_local_bear(TooManyLinesBear,
                                             valid_files=(good_file,),
                                             invalid_files=(bad_file,))

``good_file`` is a file which your bear considers as non-style-violating
and a ``bad_file`` is one which has at least one error/warning/info.
We need to write a ``good_file`` which has less than or equal to
``max_number_of_lines`` lines and a ``bad_file`` which has more than
``max_number_of_lines`` lines and feed them to ``verify_local_bear`` as input
along with your bear (TooManyLinesBear in this case) and a few additional
arguments.

.. note::

    ``good_file`` and ``bad_file`` are sequences just like ``file``. A ``file``
    is a sequence of an input file.

**EXAMPLE 2** using ``LocalBearTestHelper.check_validity``

.. code::

    from queue import Queue
    from bears.some_dir.TooManyLinesBear import TooManyLinesBear

    from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
    from coalib.settings.Section import Section
    from coalib.settings.Setting import Setting


    class TooManyLinesBearTest(LocalBearTestHelper):

        def setUp(self):
            self.section = Section('name')
            self.section.append(Setting('max_number_of_lines', '10'))
            self.uut = TooManyLinesBear(self.section, Queue())

        def test_valid(self):
            self.check_validity(self.uut, ["import os"])

        def test_invalid(self):
            self.check_validity(self.uut, bad_file, valid=False)

.. note::

    ``bad_file`` here is same as ``bad_file`` in the above example.

``check_validity`` asserts if your bear yields any results for a particular
check with a list of strings. First a *Section* and your Bear
(in this case ``TooManyLinesBear``) is ``setUp``. Now your *Section* consists
by default *Settings*. You can append any *Setting* depending on your test.
Validate a check by passing your bear, lines to check as parameters
(pass a few other parameters if necessary) to ``check_validity``. The method
``self.check_validity(self.uut, ["import os"])`` asserts if your bear
``self.uut`` yields a result when a list of strings ``["import os"]`` is
passed.

**EXAMPLE 3** using ``LocalBearTestHelper.check_results``

.. code::

    from queue import Queue

    from bears.some_dir.TooManyLinesBear import TooManyLinesBear
    from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
    from coalib.results.Result import Result
    from coalib.settings.Section import Section


    class TooManyLinesBearTest(LocalBearTestHelper):

        def setUp(self):
            self.uut = TooManyLinesBear(Section('name'), Queue())

        def test_run(self):
            self.check_results(
                self.uut,
                file,
                Result.from_values("TooManyLinesBear",
                                   "Too many lines"
                                   settings={'max_number_of_lines': int=20}))

``check_results`` asserts if your bear results match the actual
results on execution on CLI. Just like the above example, we need to ``setUp``
a *Section* and your Bear with some *Settings*. ``check_results`` validates
your results by giving your local bear, lines to check and expected results
as input. ``check_results`` asserts if your bear's results on checking the
``file`` match with ``Results.from_values(...)``.

A Final Note
------------

``LocalBearTestHelper`` is written to ease off testing for bears. Make sure
that your tests have 100% coverage and zero redundancy. Use ``check_results``
as much as possible to test your bears.
