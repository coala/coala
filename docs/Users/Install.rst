coala Installation
==================

This document contains information on how to install *coala*. Supported
platforms are Linux and Windows. *coala* is known to work on OS X as well.
*coala* is tested against CPython 3.3, 3.4 and 3.5.

In order to run *coala* you need to install Python. It is recommended,
that you install Python3 >= 3.3 from http://www.python.org.

The easiest way to install *coala* is using pip (Pip Installs Packages).
If you don't already have pip, you can install it like described on
https://pip.pypa.io/en/stable/installing.html. Note that pip is shipped
with recent python versions by default.

System wide installation
------------------------

The simplest way to install *coala* is to do it system-wide. But, This is
generally discouraged in favor or using a virtualenv.

To install the latest most stable version of *coala* and supported bears
system-wide, use:

::

    $ pip3 install coala-bears

.. note::

    For this and all future steps, some steps require root access
    (also known as administrative privileges in Windows).

    **Unix based** (Mac, Linux) - This can be achieved by using ``sudo``
    in front of the command ``sudo command_name`` instead of
    ``command_name``

    **Windows** - The easiest way on windows is to start a
    command prompt as an administrator and start ``setup.py``.

To install the nightly build from our master branch, you can do:

::

    $ pip3 install coala-bears --pre

To install only *coala* (without any bears), you can do:

::

    $ pip3 install coala

With ``--pre`` you can install the nightly build of the *coala* base
without bears.

Installing inside a virtualenv
------------------------------

Virtualenv is probably what you want to use during development,
you’ll probably want to use it there, too. You can read more about
it at their documentation - http://virtualenv.readthedocs.org

First, we need to install virtualenv to the system. This can be done
with ``pip3`` easily:

::

    $ pip3 install virtualenv

Once you have virtualenv installed, just fire up a shell and create
your own environment. I usually create a project folder and a ``venv``
folder:

::

    $ virtualenv venv

Now, whenever you want to work on the project, you only have to activate
the corresponding environment.

    On **Unix based** systems (OSX and Linux) this can be done with:

    ::

        $ source venv/bin/activate

    And on **Windows** this is done with:

    ::

        $ venv\scripts\activate

Finally, you install *coala* and supported bears inside the activated
virtualenv with:

::

    $ pip3 install coala-bears

Installing coala from source
----------------------------

In order to install *coala* from source, it is recommended to install git.
See http://git-scm.com/ for further information and a downloadable
installer or use your package manager on linux to get it.

.. note::

    Again, here it is recommended to install *coala* inside a virtualenv.
    This can be done by creating a virtualenv and running the installation
    commands after the virtualenv has been activated.

After having git installed, you can download the source code of *coala*
with the following command:

::

    $ git clone https://github.com/coala-analyzer/coala-bears/
    $ cd coala-bears

You can now install *coala* with a simple:

::

    $ python3 setup.py install

For the above to work, you may also need to install `setuptools` which can be
installed by running

::

    $ pip3 install setuptools

You will have *coala* installed into your python scripts directory. On an
unixoid system it is probably already available on your command line
globally.

You may also install a development version of *coala* to test and make
changes easily. To do this run:

::

    $ python3 setup.py develop

This essentially lets you install *coala* in a way that allows you to make
changes to the code and see the changes take effect immediately.

Alternate installation
~~~~~~~~~~~~~~~~~~~~~~

If you want to install coala to an alternate location you can e.g. call
``python3 setup.py install --prefix=/your/prefix/location``. Other
options are documented on
https://docs.python.org/3.3/install/#alternate-installation.

.. note::

    If you are using a proxy, follow these steps:

    -  Set up your system-wide proxy.
    -  Use ``sudo -E pip3 install coala`` (the ``-E`` flag takes the
       existing environment variables into the ``sudo`` environment).

    You could also set your pip.conf file to use a proxy, to know more
    read
    http://stackoverflow.com/questions/14149422/using-pip-behind-a-proxy
    for further clarification.

Error handling
~~~~~~~~~~~~~~~~

In case you are getting
``ValueError:('Expected version spec in', 'appdirs ~=1.4.0', 'at', ' ~=1.4.0')``
then don't panic. It happens when you are using an outdated version of pip
that doesn't support our version specifiers yet.


    Ideally, you have to create a virtual environment with a newer pip:

    ::

        $ pip3 install virtualenv
        $ virtualenv -p python3 ~/venvs/coala
        $ . ~/venv/coala/bin/activate
        $ pip install -U pip
        $ pip install coala-bears

You have to activate this virtualenv on every terminal session you want to use
coala though (tip: add it to bashrc!)

Dependencies
------------

This section lists dependencies of *coala* that are not automatically
installed. On Windows, you can get many with ``nuget``
(https://www.nuget.org/), on Mac Homebrew will help you installing
dependencies (http://brew.sh/).

JS Dependencies
~~~~~~~~~~~~~~~

coala features a lot of bears that use linters written in JavaScript. In
order for them to be usable, you need to install them via ``npm``
(http://nodejs.org/):

::

    $ npm install -g jshint alex remark dockerfile_lint csslint coffeelint

If a bear still doesn't work for you, please make sure that you have a
recent version of ``npm`` installed. Many linux distributions ship a
very old one.

.. note::

    If using *coala* from source you can just do ``npm install`` or
    ``npm install -g`` to use the ``package.json`` which is shipped with
    coala.

Binary Dependencies
~~~~~~~~~~~~~~~~~~~

Some bears need some dependencies available:

-  PHPLintBear: Install ``php``
-  GNUIndentBear: Install ``indent`` (be sure to use GNU Indent, Mac ships
   a non-GNU version that lacks some functionality.)
-  CSharpLintBear: Install ``mono-mcs``

Clang
~~~~~

*coala* features some bears that make use of Clang. In order for them to
work, you need to install libclang:

-  Ubuntu: ``apt-get install libclang1``
-  Fedora: ``dnf install clang-libs`` (Use ``yum`` instead of ``dnf`` on
   Fedora 21 or lower.)
-  ArchLinux: ``pacman -Sy clang``
-  Windows: ``nuget install ClangSharp``
-  OSX: ``brew install llvm --with-clang``

If those do not help you, search for a package that contains
``libclang.so``.

On windows, you need to execute this command to add the libclang path to
the *PATH* variable permanently (you need to be an administrator):

``setx PATH "%PATH%;%cd%\ClangSharp.XXX\content\x86" \M``

For x86 python or for x64 python:

``setx PATH "%PATH%;%cd%\ClangSharp.XXX\content\x64" \M``

Replace "XXX" with the ClangSharp version you received from nuget.

Generating Documentation
~~~~~~~~~~~~~~~~~~~~~~~~

*coala* documentation can be generated by fetching the documentation
requirements. This can be achieved by

::

    $ pip3 install -r docs-requirements.txt

To generate the documentation coala uses `sphinx`. Documentation can be
generated by running the following command:

::

    $ python3 setup.py docs

You can then open ``docs\_build\html\index.html`` in your favourite
browser.

See :doc:`Writing Documentation <../Getting_Involved/Writing_Documentation>`
for more information.
