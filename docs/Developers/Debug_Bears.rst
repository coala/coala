Debug Bears
===========

This document provides an overview of coala's Debugging Interface.
The Debugging Interface will help users to debug Bear code and step through
it using the pdb interface.

After invoking coala's debugger it will step into the ``run()`` method of a
bear regardless of using ``yield`` or not and will step out as soon as a bear
finish analysis.

.. note::

    Pdb's quit-command (``q``) has been remapped so coala continues its
    normal execution without aborting. So, ``quit`` or ``q`` will first clear
    all breakpoints and then continue execution.

Below is the code given for a simple ``HelloWorldBear`` that prints a debug
message for each file and yield out a message "A HelloworldBear".

.. code:: python

    import logging

    from coalib.bears.LocalBear import LocalBear


    class HelloWorldBear(LocalBear):
        def run(self, filename, file):
            logging.debug('Hello World! Checking file {}.'.
                          format(filename))

            yield self.new_result(message="A HelloworldBear",
                                  file=filename)

After invoking, the debugger will step into ``run()`` method of bear via pdb
``runcall()`` method and exits as soon as ``run()`` is left.

For example, a debug session looks like this:

::

    [DEBUG][15:58:27] Platform Linux -- Python 3.6.5, coalib
    0.12.0.dev99999999999999
    Executing section cli...
    [DEBUG][15:58:27] Files that will be checked:
    /home/Voldemort/test/mytest.py
    [DEBUG][15:58:27] coala is run only on changed files, bears' log messages
    from previous runs may not appear. You may use the `--flush-cache` flag to
    see them.
    [DEBUG][15:58:27] Running bear HelloWorldBear...
    > /home/Voldemort/coala-bears/bears/general/HelloWorldBear.py(8)run()
    -> logging.debug('Hello World! Checking file {}.'.
    (Pdb) l
    3   from coalib.bears.LocalBear import LocalBear
    4
    5
    6   class HelloWorldBear(LocalBear):
    7       def run(self, filename, file):
    8  ->           logging.debug('Hello World! Checking file {}.'.
    9                         format(filename))
    10
    11              yield self.new_result(message="A HelloworldBear.",
    12                                    file=filename)
    [EOF]
    (Pdb) c
    [DEBUG][15:58:30] Hello World! Checking file /home/Voldemort/test/mytest.py.
    --Return--
    > /home/Voldemort/coala-bears/bears/general/HelloWorldBear.py(8)run()->None
    -> logging.debug('Hello World! Checking file {}.'.
    (Pdb) c

    mytest.py
    **** HelloWorldBear [Section: cli | Severity: NORMAL] ****
    !    ! A HelloworldBear
    [    ] *0. Do (N)othing
    [    ]  1. (O)pen file
    [    ]  2. Add (I)gnore comment
    [    ] Enter number (Ctrl-D to exit):

Usage
-----

Command Line Interface
^^^^^^^^^^^^^^^^^^^^^^

Users can specify the bear they want to debug using ``--debug-bears``, i.e.

.. code:: shell

    $coala -b PEP8Bear,HelloWorldBear -f <filename> --debug-bears HelloWorldBear

If bear names are not specified for ``--debug-bears`` then it will by
default debug all the bears passed through ``--bears`` or ``-b`` argument.

.. code:: shell

    $ coala --bears HelloWorldBear -files <filename> --debug-bears

.. note::

    A bear may depend on results from different bears. The debugger will debug
    all bears on which a bear is dependent on as well.

coafile
^^^^^^^

Users can specify to debug bears using a ``.coafile``:

::

    [all]
    bears = PEP8Bear,MypyBear
    files = <filename>
    debug_bears = PEP8Bear

Or to debug all bears specified by ``bears`` setting:

::

    [all]
    bears = PEP8Bear,MypyBear
    files = <filename>
    debug_bears = True
