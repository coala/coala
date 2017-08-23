Bear Installation Tool
======================

.. note::

    cib is currently broken. Most of the commands listed here will
    not work.

coala features a Bear Installation Tool that helps installing bears one by one
or all of them. This tool is helpful as it also manages to install the bears'
external dependencies.

Installation
------------

To install the tool, simply run:

::

    $ sudo pip3 install cib

Usage
-----


To use the tool, you need to give it arguments.

To install bears, simply run ``cib install`` followed by names of bears,
or by ``all``. Therefore:

::

    $ sudo cib install all

will install all the available bears, whereas

::

    $ sudo cib install CPPCheckBear PEP8Bear

will install the specified bears only.
``cib uninstall`` works exactly the same way as ``cib install``.

To see the full list of available bears, run

::

    $ sudo cib show

To upgrade the already installed bears, run

::

    $ sudo cib upgrade all

to upgrade all installed bears, or

::

    $ sudo cib upgrade CPPCheckBear PEP8Bear

to upgrade the specified bears. However, if they are not installed, they will
not be upgraded.

``cib`` also checks for bears' dependencies, using:

::

    $ sudo cib check-deps all

For more information, run

::

    $ sudo cib help
