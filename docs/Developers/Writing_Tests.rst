Introduction
============

Tests are an essential element to check if your written components in
coala really do work like they should. Even when you think "I really
looked over my code, no need for tests" you are wrong! Bugs introduced
when not writing tests are often the most horrible ones, they have the
characteristic to be undiscoverable (or only discoverable after dozens
of hours of searching). Try to test as much as possible! The more tests
you write the more you can be sure you did everything correctly.
Especially if someone else modifies your component, they can be sure with
your tests that they don't introduce a bug. Keep these points in your mind
when you're writing a test:

- 100% test-coverage
- zero redundancy

A patch will not be accepted unless there is a 100% branch coverage.
Redundant tests are a waste of effort because you are testing the same piece
of code again and again, which is unnecessary.

Actually Writing a Test
-----------------------

So how do you implement a test in coala? First up, tests are placed into
the ``coala-bears/tests`` (if you want to write a test for a bear) or
``coala/tests`` (if you test a component written for the coalib)
directory. They are also written in Python (version 3) and get
automatically executed by running:

::

    $ pytest

There's only one constraint:
The name of the test file has to end with ``Test.py`` (for example
``MyCustomTest.py``, but not ``MyCustomTestSuite.py``).

.. note::
    If ``pytest`` seems to give errors, try running ``python3 -m pytest``
    instead.


    Often you don't want to run all available tests. To run your
    specific one, type (in the coala root folder):

    .. code:: shell

        $ pytest -k <your-test>

    You can even give partial names or queries like "not MyCustomTest"
    to not run a specific test. More information is shown with
    ``pytest -h``

Coming to the test file structure. Every test script starts with your
imports. According to the coala code style (and pep8 style) we first do
system imports (like ``re`` or ``subprocessing``), followed by first party
imports (like ``coalib.result.Result``).

Then the actual test suite class follows, that contains the tests. Each
test suite is made up of test cases, where the test suite checks the
overall functionality of your component by invoking each test case.

The basic declaration for a test suite class is as follows:

.. code:: python

    class YourComponentTest(unittest.TestCase):
        # Your test cases.
        pass

You should derive your test suite from ``unittest.TestCase`` to have
access to the ``setUp()`` and ``tearDown()`` functions (covered in
section below: **``setUp()`` and ``tearDown()``**) and also to the
assertion functions.

Now to the test cases: To implement a test case, just declare a class
member function without parameters, starting with ``test_``. Easy, isn't
it?

.. code:: python

    class YourComponentTest(unittest.TestCase):
        # Tests somethin'.
        def test_case1(self):
            pass

        # Doesn't test, this is just a member function, since the function name
        # does not start with 'test_'.
        def not_testing(self):
            pass

But how do you actually test if your component is correct? For that
purpose you have asserts. Asserts check whether a condition is fulfilled
and pass the result to the overall test-suite-invoking-instance, that
manages all tests in coala. The result is processed and you get a
message if something went wrong in your test.

.. seealso::

    `unittest assert-methods <https://docs.python.org/3/library/unittest.html#assert-methods>`_
        Documentation on the assert functions from python's inbuilt unittest.

So an example test that succeeds would be:

.. code:: python

    # The sys import and setup is not needed here because this example doesn't
    # use coala components.
    import unittest


    class YourComponentTest(unittest.TestCase):
        # Tests somethin'.
        def test_case1(self):
            # Does '1' equal '1'? Interestingly it does... mysterious...
            self.assertEqual(1, 1)
            # Hm yeah, True is True.
            self.assertTrue(True)

.. note::

    Tests in coala are evaluated against their coverage, means how many
    statements will be executed from your component when invoking your
    test cases. A branch coverage of 100% is needed for any commit in
    order to be pushed to master - please ask us on gitter if you need
    help raising your coverage!


    The branch coverage can be measured locally with the
    ``pytest --cov`` command.

    .. seealso::

        Module :doc:`Executing Tests <Executing_Tests>`
            Documentation of running Tests with coverage

    As our coverage is measured across builds against several python
    versions (we need version specific branches here and there) you will
    not get the full coverage locally! Simply make a pull request to get
    the coverage measured automatically.

    If some code is untestable, you need to mark your component code
    with ``# pragma: no cover``. Important: Provide a reason why your
    code is untestable. Code coverage is measured using python 3.4 and
    3.5 on linux.

    .. code:: python

        # Reason why this function is untestable.
        def untestable_func(): # pragma: no cover
            # Untestable code.
            pass

``setUp()`` and ``tearDown()``
------------------------------

Often you reuse components or need to make an inital setup for your
tests. For that purpose the function ``setUp()`` exists. Just declare it
inside your test suite and it is invoked automatically once at test
suite startup:

.. code:: python

    class YourComponentTest(unittest.TestCase):
        def setUp(self):
            # Your initialization of constants, operating system API calls etc.
            pass

The opposite from this is the ``tearDown()`` function. It gets invoked
when the test suite finished running all test cases. Declare it like
``setUp()`` before:

.. code:: python

    class YourComponentTest(unittest.TestCase):
        def tearDown(self):
            # Deinitialization, release calls etc.
            pass

Kickstart
---------

This section contains a concluding and simple example that you can use
as a kickstart for test-writing.

Put the code under the desired folder inside ``tests``,
modify it to let it test your stuff and run the test from
the coala root folder using ``pytest``.

.. code:: python

    # Import here your needed system components.
    import sys
    import unittest

    # Import here your needed coala components.


    # Your test unit. The name of this class is displayed in the test
    # evaluation.
    class YourTest(unittest.TestCase):
        def setUp(self):
            # Here you can set up your stuff. For example constant values,
            # initializations etc.
            pass

        def tearDown(self):
            # Here you clean up your stuff initialized in setUp(). For example
            # deleting arrays, call operating system API etc.
            pass

        def test_case1(self):
            # A test method. Put your test code here.
            pass

Glossary
--------
- ``uut`` - Unit Under Test
