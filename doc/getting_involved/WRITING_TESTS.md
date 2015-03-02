# How to Write a Test

## Introduction

Tests are an essential element to check if your written components in coala
really do work like they should. Even when you think "I really looked over my
code, no need for tests" you are wrong! Bugs introduced when not writing tests
are often the most horrible ones, they have the characteristic to be
undiscoverable (or only discoverable after dozens of hours of searching).
Try to test as much as possible! The more tests you write the more you can be
sure you did everything correct. Especially if someone else modifies your
component, he can be sure with your tests that he doesn't introduce a bug.

## Actually Writing a Test

So how do you implement a test in coala? First up, tests are placed into the
`bears/tests` (if you want to write a test for a bear) or `coalib/tests` (if
you test a component written for the coalib) directory. They are also written
in python (version 3) and get automatically executed from the global test
script, `run_tests.py`, lying in the coala root folder.
There's only one constraint: The name of the test file has to end with
`Test.py` (for example `MyCustomTest.py`, but not `MyCustomTestSuite.py`).

> **NOTE**
>
> Often you don't want to run all available tests. To run your specific one,
> type (in the coala root folder):
>
> ```shell
> ./run_tests.py -t <your-test>
> ```

Coming to the test file structure.
Every test script starts with your system imports, i.e.:

```python
# Imports the python 're' package for regex processing.
import re
# ...
```

Note that you can't import coala components here now.

After that these three lines follow:

```python
import sys
sys.path.insert(0, ".")
import unittest
```

These are necessary imports and setups to make tests working properly in the
coala testing infrastructure. They setup the paths for coala components so you
can now import them as you would do in the written component itself. Don't
change them except you know what you do.

As said before, in the next line your own imports follow. So just import what
you need from coala:

```python
import coalib.your_component.component1
import coalib.your_component.component2
# ...
```

> **NOTE**
>
> You can use system imports here also, but the coala codestyle suggests to
> place them above the three setup lines, like before.

Then the actual test suite class follows, that contains the tests. Each test
suite is made up of test cases, where the test suite checks the overall
functionality of your component by invoking each test case.

The basic declaration for a test suite class is as follows:

```python
class YourComponentTest(unittest.Test):
    # Your test cases.
    pass
```

You should derive your test suite from `unittest.Test` to have access to the
`setUp()` and `tearDown()` functions (covered in section below: **`setUp()` and
`tearDown()`**) and also to the assertion functions.

Now to the test cases: To implement a test case, just declare a class member
function without parameters, starting with `test_`. Easy, isn't it?

```python
class YourComponentTest(unittest.Test):
    # Tests somethin'.
    def test_case1(self):
        pass

    # Doesn't test, this is just a member function, since the function name
    # does not start with 'test_'.
    def not_testing(self):
        pass
```

But how do you actually test if your component is correct? For that purpose
you have asserts. Asserts check whether a condition is fulfilled and pass the
result to the overall test-suite-invoking-instance, that manages all tests in
coala. The result is processed and you get a message if something went wrong in
your test.

Available assert functions are listed in the section **Assertions** below.

At last the test file needs to end with the following sequence:

```python
if __name__ == '__main__':
    unittest.main(verbosity=2)
```

The code is only executed if your code is run as an executable. If that's the
case (like the `run_tests.py` script does), the `main()` method from the
`unittest` package is called and will execute your defined test.

So an example test that succeeds would be:

```python
# The sys import and setup is not needed here because this example doesn't use
# coala components.
import unittest


class YourComponentTest(unittest.Test):
    # Tests somethin'.
    def test_case1(self):
        # Does '1' equal '1'? Interestingly it does... mysterious...
        self.assertEqual(1, 1)
        # Hm yeah, True is True.
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
```


> **NOTE**
>
> Tests in coala are evaluated against their coverage, means how many
> statements will be executed from your component when invoking your test
> cases. You should aim at a branch coverage of 100%.
>
> If some code is untestable, you need to mark your component code with
> `# pragma: no cover`. Important: Provide a reason why your code is
> untestable.
>
> ```python
> # Reason why this function is untestable.
> def untestable_func(): # pragma: no cover
>     # Untestable code.
>     pass
> ```
>
> Code coverage is measured using python 3.4.

## `setUp()` and `tearDown()`

Often you reuse components or need to make an inital setup for your tests.
For that purpose the function `setUp()` exists. Just declare it inside your
test suite and it is invoked automatically once at test suite startup:

```python
class YourComponentTest(unittest.Test):
    def setUp(self):
        # Your initialization of constants, operating system API calls etc.
        pass
```

The opposite from this is the `tearDown()` function. It gets invoked when the
test suite finished running all test cases. Declare it like `setUp()` before:

```python
class YourComponentTest(unittest.Test):
    def tearDown(self):
        # Deinitialization, release calls etc.
        pass
```

## Skipping tests

Sometimes your test needs prerequisites the running platform lacks. That can be
either installed executables, packages, python versions etc.

coala provides two methods to skip a test.

- `skip_test()` function

  Just define this function in your test module and test the needed
  prerequisites:

  ```python
  def skip_test(self):
      # Add here your checks.
      return False

  class YourComponentTest(unittest.Test):
      pass
  ```

  The function shall only return `False` (if everything is OK and test can run)
  or a string with the reason why the test is skipped. But never return `True`!

  If your test skips, the `run_tests.py` script will show that. Note that the
  whole test module will be skipped.

  An example for skipping a test (used for the eSpeak printer test for real):

  ```python
  def skip_test():
      try:
          subprocess.Popen(['espeak'])
          return False
      except OSError:
          return "eSpeak is not installed."
  ```

- `unittest` built-in attributes

  The `unittest` package from python defines attributes to handle skips for
  specific test cases, not only the whole test suite.

  Skipping tests using attributes **is not shown** in the `run_tests.py`
  script!

  Since there are many ways to skip tests like this, here only a short example:

  ```python
  @unittest.skipIf(mylib.__version__ < (1, 3),
                   "Not supported in this library version.")
  def test_format(self):
      # Tests that work for only a certain version of the library.
      pass
  ```

  For more information about the attribute usage, refer to the [documentation]
  (https://docs.python.org/3.4/library/unittest.html) at paragraph
  **26.3.6. Skipping tests and expected failures**.

## Assertions

Here follows a list of all available assertion functions supported when
inheriting from `unittest.Test`:

- `assertEqual(a, b)`

  Checks whether expression `a` equals expression `b`.

- `assertNotEqual(a, b)`

  Checks whether expression `a` **not** equals expression `b`.

- `assertTrue(a)`

  Checks whether expression `a` is True.

- `assertFalse(a)`

  Checks whether expression `a` is False.

- `assertIs(a, b)`

  Checks whether expression `a` is `b`.

- `assertIsNot(a, b)`

  Checks whether expression `a` is not `b`.

- `assertIsNone(a)`

  Checks whether expression `a` is None.

- `assertIsNotNone(a)`

  Checks whether expression `a` is not None.

- `assertIn(a, list)`

  Checks whether expression `a` is an element inside `list`.

- `assertNotIn(a, list)`

  Checks whether expression `a` is not an element inside `list`.

- `assertIsInstance(a, type)`

  Checks whether expression `a` is of type `type`.

- `assertNotIsInstance(a, type)`

  Checks whether expression `a` is not of type `type`.

- `assertRaises(error, function, *args, **kwargs)`

  Checks whether `function` throws the specific `error`. When calling this
  assert it invokes the function with the specified `*args` and `**kwargs`.

If you want more information about the python `unittest`-module, refer to the
[official documentation](https://docs.python.org/3/library/unittest.html) and
for asserts the subsection [assert-methods]
(https://docs.python.org/3/library/unittest.html#assert-methods).

## Kickstart

This section contains a concluding and simple example that you can use as a
kickstart for test-writing.

Put the code under the desired folder inside `coalib/tests` or `bears/tests`,
modify it to let it test your stuff and run from the coala root folder
`./run_tests.py`.

```python
# Import here your needed system components.

import sys
sys.path.insert(0, ".")
import unittest

# Import here your needed coala components.


# Your test unit. The name of this class is displayed in the test evaluation.
class YourTest(unittest.Test):
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


if __name__ == '__main__':
    unittest.main(verbosity=2)

```

