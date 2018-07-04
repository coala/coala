coala's IO Mechanism
====================

Instead of directly loading files from a project directory coala uses a
class called ``FileFactory`` that provides an interface for dealing with
files.

``FileFactory`` provides the following advantages as compared to simple file
loading.

- Lazy-loading of files: Files don't have to be immediately loaded into the
  memory, instead coala collects all the ``FileFactory`` objects first which
  are in turn used to access the file contents when needed.
- Contents can be accessed in various formats: ``FileFactory`` provides the
  option to access the file contents in three formats. As a string using
  ``FileFactory.string``, as a list using ``FileFactory.lines`` and in raw
  format using ``FileFactory.raw``. To access a particular line in the file one
  can use``FileFactory.line(line_number)``. Another benefit of storing the raw
  file contents is the ability to easily deploy analysis that works on raw files
  only. Since the contents are not decoded as long as ``FileFactory.string``
  is not called we don't need to have a separate mode for using raw files
  anymore.
- High Performance: ``FileFactory``'s properties are cached to reduce
  unnecessary load caused by accessing the same property multiple times.


Caching
-------

``FileFactory`` uses ``cached_property`` to decorate its
properties. Due to this the properties are only called once for the first
time and then their results are stored in a cache which is tied to the
same ``FileFactory`` object. If the properties are accessed again for the
same object then a cache lookup is performed and the contents are served
without loading the file again. Once the ``FileFactory`` object is destroyed
the cache is also destroyed with it.
