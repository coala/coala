Profile Bears
=============

This document provides an overview of coala's Profiling Interface. The
Profiling Interface provides abilities to profile Bear code to optimize its
performance.

The profiler will start by profiling the run() method of bears because this is
the part where bear writers will spend time on, as rest of the part like loading
the files, collecting the settings, etc. are done by coala itself.

.. note::

    Enabling both profiler and debugger on a bear at the same time will result
    in error.

Bear writers will have the ability to directly dump the raw profile output
either on current working directory or to a specified directory name, which can
be further used for examination of profiler stats with the help of different
modules like ``pstats`` or ``snakeviz``.

Usage
-----

coala's Profiler accepts an additional parameter, a directory path where
profiled data files will be dumped.

If no any directory specified, profiled files will be saved to current working
directory. If the specified directory does not exist it will be created. If the
specified path points to an already existing file a error is raised.

Profiled files will get overwritten, if specified directory already had a
profiled data files in it.

.. note::

    All bears (even implicit dependency bears) in a section will be profiled.
    Profiled data files will have a name format
    ``{section.name}_{bear.name}.prof``.

Command Line Interface
^^^^^^^^^^^^^^^^^^^^^^

Bear writers can invoke the profiler with the ``--profile`` argument.

- To dump profile files in current working directory:

  .. code:: shell

      $coala -b PEP8Bear,PyUnusedCodeBear -f <filename> --profile

- To dump profile files to a specified directory:

  .. code:: shell

      $coala -b PEP8Bear,MypyBear -f <filename> --profile <dirpath>

coafile
^^^^^^^

Users can specify to profile bears using a ``.coafile`` as well.

- To dump profile files in current working directory:

  ::

      [all]
      bears = PEP8Bear,MypyBear
      files = <filename>
      profile = True

- To dump profile files to a specified directory:

  ::

      [all]
      bears = PEP8Bear,MypyBear
      files = <filename>
      profile = dirpath
