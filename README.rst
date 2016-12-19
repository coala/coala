.. image:: https://cloud.githubusercontent.com/assets/7521600/15992701/ef245fd4-30ef-11e6-992d-275c5ca7c3a0.jpg

coala: Linting and fixing code for all languages
------------------------------------------------

**coala provides a unified command-line interface for linting and fixing all
your code, regardless of the programming languages you use.**

With coala, users can create
`rules and standards <http://docs.coala.io/en/latest/Users/coafile.html>`__
to be followed in the source
code. coala has an **user-friendly interface** that is completely customizable.
It can be used in any environment and is completely modular.

coala has a set of official bears (plugins) for several languages, including
popular languages such as **C/C++**, **Python**, **JavaScript**, **CSS**,
**Java** and many more, in addition to some generic language independent
algorithms. To learn more about the different languages supported and the
bears themselves,
`click here. <https://github.com/coala/bear-docs/blob/master/README.rst>`__

To see what coala can do for your language, run:

.. code-block:: bash

    $ coala --show-bears --filter-by-language Python

|Linux Build Status| |Windows Build status| |Scrutinizer Code Quality|
|codecov.io| |Documentation Status| |Gitmate|

.. Start ignoring LineLengthBear

======================================= ========================================= ================================================= ====================================================== =========================================================
`Official Website <http://coala.io/>`__ `Documentation <https://docs.coala.io>`__ `Twitter <https://twitter.com/coala_analyzer>`__  `Facebook <https://www.facebook.com/coalaAnalyzer/>`__ `Video Demo <https://asciinema.org/a/42968?autoplay=1>`__
======================================= ========================================= ================================================= ====================================================== =========================================================

.. Stop ignoring

-----

.. contents::
    :local:
    :depth: 1
    :backlinks: none

-----

========
Features
========

* Out-of-the-box support for various `popular languages <https://github.com/coala/bear-docs/blob/master/README.rst>`__,
  such as **C/C++**, **Python**, **Javascript**, **CSS**, **Java** and many
  others with built-in check routines.
* User-friendly interfaces such as JSON, interactive CLI or any custom format.
* Plugins for
  `gedit <https://github.com/coala/coala-gedit>`__,
  `Sublime Text <https://github.com/coala/coala-sublime>`__,
  `Atom <https://github.com/coala/coala-atom>`__,
  `Vim <https://github.com/coala/coala-vim>`__ and
  `Emacs <https://github.com/coala/coala-emacs>`__.
* Optimized performace with multi-threading to parallelize the routines - can
  complete a 26000 line python repository in less than 3 seconds.
* File caching support - run only on changed files.

-----

============
Installation
============

To install the **latest stable version** run:

.. code-block:: bash

    $ pip3 install coala

**Make sure you have Python >= 3.4 and pip >= 6 installed.**

|Stable|

To install the latest development version run:

.. code-block:: bash

    $ pip3 install coala --pre

The latest code from the master branch is automatically deployed as the
development version in PyPI.

To also install all bears for coala at once run:

.. code-block:: bash

    $ pip3 install coala-bears

You can also use ``cib`` (coala Installs Bears), which is an experimental bear
manager that lets you install, upgrade, uninstall, check dependencies, etc.
for bears. To install it, run:

.. code-block:: bash

    $ pip3 install cib

For usage instructions, consult
`this link <http://api.coala.io/en/latest/Developers/Bear_Installation_Tool.html>`__.

|PyPI| |Windows| |Linux|

-----

=====
Usage
=====

There are two options to run coala:

* using a ``.coafile``, a project specific configuration file that will store
  all your settings for coala
* using command-line arguments

Using a ``.coafile``
********************

A sample ``.coafile`` will look something like this:

.. code-block:: bash

    [Spacing]
    files = src/**/*.py
    bears = SpaceConsistencyBear
    use_spaces = True

* The ``files`` key tells coala which files to lint - here we're linting all
  python files inside the ``src/`` directory by using a glob expression.
* The ``bears`` key specifies which bears (plugins) you want to use. We support
  a huge number of languages and you can find the whole list
  `here <https://github.com/coala/bear-docs/blob/master/README.rst>`__.
  If you don't find your language there, we've got some
  `bears that work for all languages <https://github.com/coala/bear-docs/blob/master/README.rst#all>`__. Or you can file an issue and we would create a bear for you!
* ``use_spaces`` enforces spaces over tabs in the codebase. ``use_spaces`` is a
  setting for the ``SpaceConsistencyBear`` defined
  `here <https://github.com/coala/bear-docs/blob/master/docs/SpaceConsistencyBear.rst>`__.

``[Spacing]`` is a *section*. Sections are executed in the order you
define them.

Store the file in the project's root directory and run coala:

.. code-block:: bash

    $ coala

Please read our
`coafile specification <http://docs.coala.io/en/latest/Users/coafile.html>`__
to learn more.

Using command-line arguments
****************************

However, if you don't want to save your settings, you can also run coala with
command line arguments:

.. code-block:: bash

    $ coala --files=setup.py --bears=SpaceConsistencyBear -S use_spaces=True

Note that this command does the same thing as having a coafile and running
`coala`. The advantage of having a coafile is that you don't need to enter the
settings as arguments everytime.

To get the complete list of arguments and their meaning, run:

.. code-block:: bash

    $ coala --help

You can find a quick demo of coala here:

|asciicast|

.. |asciicast| image:: https://asciinema.org/a/42968.png
   :target: https://asciinema.org/a/42968?autoplay=1
   :width: 100%

-----

======
Awards
======

.. image:: http://www.yegor256.com/images/award/2016/winner-sils.png
   :alt: Awards - Yegor256 2016 Winner

-----

================
Getting Involved
================

If you would like to be a part of the coala community, you can check out our
`Getting In Touch <http://docs.coala.io/en/latest/Help/Getting_In_Touch.html>`__
page or ask us at our active Gitter channel, where we have maintainers from
all over the world. We appreciate any help!

We also have a
`newcomer guide <http://coala.io/newcomer>`__
to help you get started by fixing an issue yourself! If you get stuck anywhere
or need some help, feel free to contact us on Gitter or drop a mail at our
`newcomer mailing list <https://groups.google.com/d/forum/coala-newcomers>`__.

|gitter|

-----

=======
Support
=======

Feel free to contact us at our `Gitter channel <https://gitter.im/coala/coala>`__, we'd be happy to help!

You can also drop an email at our
`mailing list <https://github.com/coala/coala/wiki/Mailing-Lists>`__.

-----

=======
Authors
=======

coala is maintained by a growing community. Please take a look at the
meta information in `setup.py <setup.py>`__ for the current maintainers.

-----

=======
License
=======

|AGPL|

.. |Windows| image:: https://img.shields.io/badge/platform-Windows-brightgreen.svg
.. |Linux| image:: https://img.shields.io/badge/platform-Linux-brightgreen.svg
.. |Stable| image:: https://img.shields.io/badge/latest%20stable-0.9.0-green.svg
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/coala.svg
   :target: https://pypi.python.org/pypi/coala
.. |Linux Build Status| image:: https://img.shields.io/circleci/project/coala/coala/master.svg?label=linux%20build
   :target: https://circleci.com/gh/coala/coala
.. |Windows Build status| image:: https://img.shields.io/appveyor/ci/coala/coala/master.svg?label=windows%20build
   :target: https://ci.appveyor.com/project/coala/coala/branch/master
.. |Scrutinizer Code Quality| image:: https://img.shields.io/scrutinizer/g/coala-analyzer/coala.svg?label=scrutinizer%20quality
   :target: https://scrutinizer-ci.com/g/coala-analyzer/coala/?branch=master
.. |codecov.io| image:: https://img.shields.io/codecov/c/github/coala/coala/master.svg?label=branch%20coverage
   :target: https://codecov.io/github/coala/coala?branch=master
.. |Documentation Status| image:: https://docs.coala.io/projects/coala/badge/?version=latest
   :target: http://coala.rtfd.org/
.. |AGPL| image:: https://img.shields.io/github/license/coala/coala.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html
.. |Gitmate| image:: https://img.shields.io/badge/Gitmate-0%20issues-brightgreen.svg
   :target: http://gitmate.com/
.. |gitter| image:: https://badges.gitter.im/coala/coala.svg
    :target: https://gitter.im/coala/coala
    :alt: Chat on Gitter
