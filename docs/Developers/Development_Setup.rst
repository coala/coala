.. _dev-notes:

Development Setup Notes
=======================

The following are some useful notes for setting up an environment to work on
coala.

Virtualenv
----------

We highly recommend installing coala in a virtualenv for development. This
will allow you to have a contained environment in which to modify coala,
separate from any other installation of coala that you may not want to
break. For more information about virtualenvs, please refer to the
`virtualenv setup <https://docs.coala.io/en/latest/Help/MAC_Hints.html#create-virtual-environments-with-pyvenv>`__ section for information on setting one
up.

Repositories
------------

If you are interested in contributing to coala, we recommend that you read
our :ref:`newcomers' guide <newcomer-guide>` to familiarize yourself with our
workflow, and perhaps with GitHub itself.

You will most likely need to work only in the ``coala`` or ``coala-bears``
repository. The former is the core of coala, and the latter contains the set
of standard bears. You can fork and clone the repositories from:

https://github.com/coala/coala

https://github.com/coala/coala-bears

Installing from Git
-------------------

We recommend first installing the latest development snapshot of coala's
master branch from and all of its dependencies with pip using

::

    (venv)$ pip3 install coala-bears --pre

Then you can install a repository-backed version of the repository you would
like to modify using

::

    (venv)$ pip3 install -e <path/to/clone>

You will then be able to edit the repository and have the changes take effect
in your virtualenv immediately. You will also be able to use pip to manage
your installation of the package should you need to install from a different
source in the future.


Building Documentation
----------------------

You will need to install the following packages to build the documentation:

::

    (venv)$ pip3 install sphinx sphinx_rtd_theme

Once you have done so, you can build the documentation by entering the docs
directory and running ``make``. The documentation on the coala website is in
the ``coala`` (not ``coala-bears``) repository.
