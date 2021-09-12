Testing
=======

You can help us test coala in several ways.

Executing our Tests
-------------------

coala has a big test suite. It is meant to work on every platform on
every PC. If you just execute our tests you are doing us a favour.

To run tests, You first need to install some dependencies.
This can be done by following these steps:

If you have not already, clone the
`repository <https://github.com/coala/coala>`_ (or a fork of
it) by running:

::

    $ git clone https://github.com/coala/coala

Navigate to the directory where coala is located.

Next, you need to install some requirements. This can be
done by executing the following command while in the root of the
coala project directory.

::

    $ pip3 install -r test-requirements.txt -r requirements.txt

You can then execute our tests with

::

    $ pytest

.. note::
    If ``pytest`` seems to give errors, try running ``python3 -m pytest``
    instead.

and report any errors you get!

To run our tests, you can also use ``python3 setup.py test``

.. note::

    If you need to customize test running, you can get more options
    about allowing skipped tests, getting code coverage displayed
    or omitting/selecting tests using ``pytest`` directly.

    ::

        $ pytest --help

.. note::

    You may not get a test coverage of 100% locally. The coverage
    published on `codecov.io <https://codecov.io/gh/coala/>`__ (GitHub
    Projects) and `codecov.io <https://codecov.io/gl/coala/>`__ (GitLab
    Projects) are actually merged results for several python versions.
    The results are merged from different OS. Appveyor results
    provide coverage of Windows specific lines, and Travis/Circle
    provide coverage of Unix specific lines. Also, the lack of tests that
    developers often forget to write is typically why one will see test
    coverage not reach 100%. Thus, your test coverage can 'pass' without
    reaching 100%. If you make changes to the code, then you should
    concentrate on getting 100% coverage on the changes made rather than
    worrying about the coverage of the whole project.

Using test coverage
-------------------

To get coverage information, you can run:

::

    $ pytest --cov

You can view the coverage report as html by running:

::

    $ pytest --cov --cov-report html

The html report will be saved ``.htmlreport`` inside the coala repository.
