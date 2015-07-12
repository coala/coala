# Testing

You can help us testing coala in several ways.

# Executing our Tests

coala has a big test suite. It is meant to work on every platform on every PC.
If you just execute our tests you are doing us a favor. You can execute our
tests with our `./run_tests.py` script and report any errors you get!

If you need more options about allowing skipped tests, getting code coverage
displayed or omitting/selecting tests, just query `./run_tests.py --help`.
Please note that you will not get a test coverage of 100% - the coverage on the
website is merged for several python versions.

# Using test coverage

To get coverage information, you can run `./run_tests.py --cover`. To do so you
need to install the `coverage` package via pip:

```
pip install coverage
```
