"""
The core package provides an API for coala's NextGen-Core.

The ``Core`` module is responsible for maintaining sessions for coala's
execution and also running the tasks offloaded by the bears. The ``Bear``
module provides a base class for all the NextGen Bears.

``FileBear`` provides a Bear base class to parallelize tasks for each file.
``ProjectBear`` on the other hand provides a base class for bears that run on
the whole codebase.

``DependencyBear`` is a Bear base class that parallelizes tasks for dependency
results. The ``DependencyTracker`` module registers and manages dependencies
between objects. The circular dependency errors are handled by
``CircularDependencyError``. The ``Graphs`` detects cyclicity in dependency
graphs and raises ``CircularDependencyError`` if found.

``PersistentHash`` module generates a unique hash for every task object
first by pickling them and then using the pickled object to generate a sha1
hash. It can then be used for caching results.
"""
