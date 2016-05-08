Exit Codes
==========

The following is a list of ``coala``'s exit codes and their meanings:

-  ``0`` - ``coala`` executed successfully but yielded no results.
-  ``1`` - ``coala`` executed successfully but yielded results.
-  ``2`` - Invalid arguments were passed to ``coala`` in the command line.
-  ``3`` - The file collector exits with this code if an invalid pattern
   is passed to it.
-  ``4`` - ``coala`` was executed with an unsupported version of python
-  ``5`` - ``coala`` executed successfully. Results were found but patches
   to the results were applied successfully
-  ``13`` - There is a conflict in the version of a dependency you have
   installed and the requirements of ``coala``.
-  ``130`` - A ``KeyboardInterrupt`` (``Ctrl+C``) was pressed during the
   execution of ``coala``.
-  ``255`` - Any other general errors.
