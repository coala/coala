.. Start ignoring LineLengthBear

::

                                                         .o88Oo._
                                                        d8P         .ooOO8bo._
                                                        88                  '*Y8bo.
                                          __            YA                      '*Y8b   __
                                        ,dPYb,           YA                        68o68**8Oo.
                                        IP'`Yb            "8D                       *"'    "Y8o
                                        I8  8I             Y8     'YB                       .8D
                                        I8  8P             '8               d8'             8D
                                        I8  8'              8       d8888b          d      AY
         ,gggo,    ,ggggo,    ,gggo,gg  I8 dP    ,gggo,gg   Y,     d888888         d'  _.oP"
        dP"  "Yb  dP"  "Y8go*8P"  "Y8I  I8dP    dP"  "Y8I    q.    Y8888P'        d8
       i8'       i8'    ,8P i8'    ,8I  I8P    i8'    ,8I     "q.  `Y88P'       d8"
      ,d8,_    _,d8,   ,d8' d8,   ,d8b,,d8b,_ ,d8,   ,d8b,       Y           ,o8P
    ooP""Y8888PP*"Y8888P"   "Y8888P"`Y88P'"Y88P"Y8888P"`Y8            oooo888P"

.. Stop ignoring LineLengthBear

Get coala to lint all your languages in your project with one tool and config!

Demo (Click to View)
--------------------

|asciicast|

.. |asciicast| image:: https://asciinema.org/a/42968.png
   :target: https://asciinema.org/a/42968?autoplay=1
   :width: 100%

About
-----

*coala* is a language independent analysis toolkit. It empowers developers
to create rules which a project's code should conform to. coala takes care
of showing these issues to users in a friendly manner, is versatile and can be
used in any environment. Patches to automatically fix code will be managed too.
*coala* has a set of official bears (plugins) to provide an out-of-the-box
analysis functionality for many popular languages in addition to some
generically applicable algorithms.

For information on the languages supported by *coala-bears*, refer to
`this link <https://github.com/coala-analyzer/coala-bears/wiki/Supported-languages>`__.

For information on the various bears supported by *coala*, refer to the link
`here <https://github.com/coala-analyzer/coala-bears/wiki/Available-bears>`__.

*coala* is written with a lower case "c".

Read more at our `documentation <http://coala.rtfd.org/>`__.

Why use coala?
--------------

- *coala* provides **built-in checking routines** (named bears in *coala*).
- **Serves your requirement**: You can easily write your own checks (using
  bears).
- *coala* provides **user-friendly interfaces** like json, formatted and
  interactive output in the CLI and *plugins for various editors* are
  available as well.
- **Optimal performance**: *coala* manages parallelizing the checking-routines
  without you having to worry.
- **Unified interface**: One tool for all programming languages.

If you want to learn more about *coala*, its functionality and its usage,
please take a look at our
`tutorial <http://coala.rtfd.org/en/latest/Users/Tutorials/Tutorial.html>`__.

Installation
------------

To install *coala* with the official set of analysis routines you can simply run
``pip3 install coala-bears``.

*coala* only, without the official bears, can be installed with
``pip3 install coala``. If you need more information about the installation and
dependencies, take a look at our `installation documentation
<http://coala.rtfd.org/en/latest/Users/Install.html>`__.

The latest code from master is automatically deployed to PyPI as a
development version. Get it with ``pip3 install coala --pre``.

|PyPI|

Authors
-------

*coala* is maintained by a growing community. Please take a look at the
meta information in `setup.py <setup.py>`__ for current maintainers.

Project Status
--------------

|Linux Build Status| |Windows Build status| |OSX Build status|

|Scrutinizer Code Quality| |codecov.io|

|Documentation Status| |Gitmate|

Newcomers Guide and Getting Involved
------------------------------------

If you are new and would like to contribute, read our `Getting Involved Site
<http://coala.readthedocs.org/en/latest/Getting_Involved/README.html>`__!

We appreciate any help! Feel free to message us on
`gitter <https://gitter.im/coala-analyzer/coala>`__. If you have any
questions we're happy to help you!


License
-------

|AGPL|

This code falls under the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

Please note that some files or content may be copied from other places.
Most of them are GPL compatible. There is a small portion of code in the
tests that falls under the Creative Commons license, see
https://creativecommons.org/licenses/by-sa/3.0/deed.de for more
information.

.. |PyPI| image:: https://img.shields.io/pypi/pyversions/coala.svg
   :target: https://pypi.python.org/pypi/coala
.. |Linux Build Status| image:: https://img.shields.io/circleci/project/coala-analyzer/coala/master.svg?label=linux%20build
   :target: https://circleci.com/gh/coala-analyzer/coala
.. |Windows Build status| image:: https://img.shields.io/appveyor/ci/coala/coala/master.svg?label=windows%20build
   :target: https://ci.appveyor.com/project/coala/coala/branch/master
.. |Scrutinizer Code Quality| image:: https://img.shields.io/scrutinizer/g/coala-analyzer/coala.svg?label=scrutinizer%20quality
   :target: https://scrutinizer-ci.com/g/coala-analyzer/coala/?branch=master
.. |codecov.io| image:: https://img.shields.io/codecov/c/github/coala-analyzer/coala/master.svg?label=branch%20coverage
   :target: https://codecov.io/github/coala-analyzer/coala?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/coala/badge/?version=latest
   :target: http://coala.rtfd.org/
.. |https://gitter.im/coala-analyzer/coala| image:: https://img.shields.io/badge/gitter-join%20chat%20%E2%86%92-brightgreen.svg
   :target: https://gitter.im/coala-analyzer/coala
.. |AGPL| image:: https://img.shields.io/github/license/coala-analyzer/coala.svg
   :target: https://www.gnu.org/licenses/agpl-3.0.html
.. |Gitmate| image:: https://img.shields.io/badge/Gitmate-0%20issues-brightgreen.svg
   :target: http://gitmate.com/
