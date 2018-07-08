NextGen-Core
============

This document provides a brief overview of coala's NextGen-Core.
coala's NextGen-Core comes with the promise of lifting many limitations of the
old core and better efficiency and performance.

What is new?
------------

The following new features have been added as a part of the NextGen-Core:

- Easier Interface
- Official support for virtual files
- Improved dependency system
- New base bear type: ``DependencyBear``
- Ability to modify bear dependencies at runtime
- Superior caching

What has changed?
-----------------

- ``Global Bears`` are now called ``Project Bears`` and ``Local Bears`` are
  now known as ``File Bears``. Both the ``ProjectBear`` and the ``FileBear``
  classes inherit from the new base class ``coalib.core.Bear``.
- There is no need to pass ``HiddenResults`` between different bears (made
  possible by the new dependency management system) to hide results to the
  result callback. Only the results that were explicitly requested by passing
  the needed bears are passed now. The dependency bears can pass arbitrary
  python objects, not just the ``Result`` objects.
- The former ``run`` function that was inherited by all the bears to run code
  analysis is now replaced by the ``analyze`` function.

Easier Interface
----------------

Running a coala session with the NextGen-Core can be done by accessing
only one function, ``core.run(bears)``. The ``run`` method takes the
arguments ``bears``, ``result_callback``, ``cache`` and ``executor``
(the last two are ``None`` by default) and initiates a coala session.

* The ``bears`` argument contains the list of bears to be run for a coala
  session.
* The ``result_callback`` is a function that is called on each result as soon as
  it's available. It should have the following signature:

  ::

      def result_callback(result):
          pass

* The ``cache`` argument if provided enables caching and runs the session using
  the cache provided to store the bear results. The default value of this
  parameter is ``None`` which when provided, runs coala without a cache.
* The ``executor`` argument is used to provide a custom executor (which is
  closed after the core is closed) in which the passed bears are to be run.
  If this argument is not provided then ``ProcessPoolExecutor`` is used using as
  many processes as cores available on the system.

Bears in the NextGen-Core are implemented differently as compared to the old
bears. Following points must be kept in mind while writing NextGen bears:

* Every bear has an ``analyze`` function to perform code
  analysis instead of the ``run`` function that was there in the old bears.
* The new bears must be able to be constructed with ``section`` and
  ``file_dict`` as parameters. Default parameters are allowed but discouraged,
  as you have no control over them when your bear is used as a dependency.

  ::

      class TestBear(Bear):

      def analyze(self, bear, section_name, file_dict):
          return "Some analysis"

More details can be found at the `API Docs <http://api.coala.io/>`_.

Official support for virtual files
----------------------------------

IDEs like IntelliJ use virtual files to represent files in a filesystem (VFS)
and perform operations on them. Hence NextGen-Core provides official support
for virtual files. Bears have to point to the right file data objects when
run, whether they are real files or virtual ones. This makes coala easier to
integrate with IDEs.

Task Objects
------------

Task objects are the representation of tasks performed by bears. Structure-wise
they are a tuple containing tuples of positional arguments and dicts of
keyword arguments to the ``execute_task`` function, which itself calls
``analyze`` with them caching mechanism as their hash values are stored in the
cache along with the bear results and are looked up during each coala run to
fetch the results.

To get a clear picture of what task objects for a bear might look like take a
look at the following example ``FileBear``:

::

    from coalib.core.FileBear import FileBear


    class SomeFileBear(FileBear):

        def analyze(self, file, filename, filename_prefix: str='',
                    filename_suffix: str=''):
            yield 'Some analysis result'

Its corresponding task object would look like the one below:

::

    [
        [(file, filename), {'filename_prefix': "", 'filename_suffix': ""}],
    ]

These task objects can then be offloaded by bears to be executed in a Python
pool by the ``generate_tasks`` method.

Improved Dependency System
--------------------------

The NextGen-Core introduces a better dependency management system than the
one used by the old core. It features following improvements:

* A bear specifies its bear dependencies in ``BEAR_DEPS``.
* A class ``DependencyTracker`` manages dependency management. Dependencies are
  added and resolved by this class and it checks for circular dependencies.
* Dependency relations between two objects are tracked using a directed graph.
  When two nodes are connected with a directed edge they form a dependency
  relation. The NextGen-Core lifts the limitation of specifying ``LocalBear``\s
  as dependencies of ``GlobalBear``\s.

The ``initialize_dependencies`` method in ``Core`` receives the bears that
are to be run and processes bear dependencies using a consumer-based system so
that each dependency bear has only one instance per section and file-dict. It
returns a set of dependency bears along with those bears that don't have any
dependencies or whose dependencies have been resolved (these are the ones that
are scheduled to be run). Before the bears are run we initialize the dependency
tracking in the ``__init__`` method of the class ``Session`` which is
responsible for running coala sessions.

The bears that have no dependencies or whose dependencies have been resolved,
only their tasks will be scheduled for execution. Before executing any task
coala looks it up in the cache. In case of a hit, the existing results that are
stored in the cache for the corresponding task arguments are called using
``execute_task_with_cache`` method. In case of a miss or if coala is run without
a cache the task is executed. The bears without any running tasks are cleaned up
from the state of an ongoing run by resolving its dependencies, scheduling
dependent bears and removing the bear from the ``running_tasks`` dict.

Even though bears still have to pass ``Result`` instances to communicate with
coala, it is now possible to pass arbitrary Python objects. Dependency bears
benefit from this because now they can pass data according to their needs
without being bound to ``Result`` objects only.

The dependency results lie inside ``self.dependecy_results`` and can be accessed
that way. **But this is highly discouraged since it bypasses caching and
could yield unexpected results when the core is run multiple times in a row.**

DependencyBear
--------------

Handling of bear dependencies by the old core wasn't effective. The
old core used a queuing mechanism to communicate between bear runs. The
NextGen-Core improves on this.

A new bear type was introduced, ``DependencyBear``, makes it more convenient
for bear developers to write dependency bears, by passing the dependency results
using task objects. This technique of handling dependencies make it possible for
the ``DependencyBear`` to support caching.

This bear serves as a base class which parallelizes tasks for each dependency
result. A bear dependent on other bears can specify its dependencies in
``BEAR_DEPS``. For example, there are two bears ``Foo`` and ``Bar``
and bear ``Bar`` depends on ``Foo``. This can be written as

::

    class BarBear(DependencyBear):
        BEAR_DEPS = {FooBear}

This solves the dependency issues of ``GlobalBear``\s on ``LocalBear``\s that
were there in the old core. Now that the new dependency management is in place
``GlobalBear``\s won't be stalled due to the termination of a LocalBear run.
This eradicates all the synchronization problems faced by the old core.

Multiple bears can be included as a dependency of a bear in the ``BEAR_DEPS``
field. The results of the dependency bears are saved in a dictionary
called ``_dependency_results`` which is initialized in the ``__init()__``
method of the class ``Bear`` and can be accessed using the method
``dependency_results()`` also belonging to the same class.

Writing a DependencyBear
------------------------

Let's consider a bear to be dependent on a project bear ``Fizz`` and a file bear
``Buzz`` then the corresponding DependencyBear let's call it ``FizzBuzz`` will
look like the following:

::

    class FizzBear(ProjectBear):

        def analyze(self, file, filename):
            yield 'Fizz analysis'

::

    class BuzzyBear(FileBear):

        def analyze(self, file, filename):
            yield 'Buzz analysis'

::

    class FizzBuzzBear(DependencyBear):
        BEAR_DEPS = {FizzBear, BuzzBear}

        def analyze(self, dependency_bear, dependency_result, a_number=100):
            yield '{} ({}) - {}'.format(
                dependency_bear.name, a_number, dependency_result)

Ability To Modify Bear Dependencies At Runtime
----------------------------------------------

A bear might depend on multiple bears before its execution can begin.
``Bear.BEAR_DEPS`` is just a set of bear classes that need to be executed
before that bear can run. Once all these dependencies have run, their
results are appended to ``self.dependency_results``. The results are in the form
of a dictionary with the types of the bears and their corresponding results
(in the form of a list) as *key-value* pairs. From the previous example if we
try to access the BEAR_DEPS of the ``BarBear`` we will get the result
``{<class 'coalib.core.Bear.FooBear'>}``.

In the `__init__()` method of the class ``Bear`` the dependencies specified
in the ``BEAR_DEPS`` are copied to every instance of a Bear run using
which makes runtime modifications possible.

Override bears
--------------

A NextGen bear has to have the following functions to perform analysis:

- ``analyze``: This method contains the code that performs the actual code
  analysis routine that that bear is used for.

- ``generate_tasks``: This method is a part of the parent ``Bear`` class
  and returns tuples containing the positional arguments as a tuple and the
  keyword arguments in the form of a dict. These are actually the task objects
  that are scheduled and executed by the core. An absence of this method raises
  ``NotImplementedError``(one thing to be kept in mind is that you need to
  implement a ``generate_task`` only if the other bear base classes don't offer
  the right parallelization level.) .

A bear inheriting from the class ``FileBear`` can parallelize tasks for each
file given. A bear inheriting from the class ``DependencyBear`` can
parallelize tasks for each dependency result. A bear inheriting from the class
``ProjectBear`` does not parallelize tasks for each file as it runs on the
whole codebase given.

Let's write our own bears with custom ``generate_tasks`` methods. We will call
this bear ``PairWiseDependencyBear`` which will compare the results from
genereted by two of its dependency bears. (This kind of bear might be useful
in case of code clone detection).

::

    # This bear provides some code analysis
    class SomeDependencyBear(Bear):

        def analyze(self, bear, section_name, file_dict):
            yield 'Some analysis result'

::

    # This bear provides some code analysis
    class SomeOtherDependencyBear(Bear):

        def analyze(self, bear, section_name, file_dict):
            yield 'Some more analysis result'

::

    # This bear depends on the above bear and performs some
    # more analysis after receving its results
    class PairWiseDependencyBear(Bear):
        BEAR_DEPS = {SomeDependencyBear, SomeOtherDependencyBear}

        def analyze(self, file, filename):
            return 'More analysis'

        def generate_tasks(self):
            similar_results = []
            results = [r['SomeDependencyBear'] for r in self.dependecy_results]
            other_results = [r['SomeOtherDependencyBear']
                       for r in self.dependecy_results]

            for a, b in zip(results, other_results):
                if a == b:
                    similar_results = a

            # returns some kind of task object containing
            # the results common to both dependency bears
            # and their corresponding lengths
            return (((i, len(i)), {}) for i in similar_results)

Superior Caching
----------------

NextGen-Core's caching can be broken up into two parts:

- Caching of ``FileFactory`` objects
- Caching of task objects

Since NextGen-Core passes bears ``FileFactory`` objects to interface with
files, ``FileFactory`` uses its own caching mechanism to ensure
high performance I/O operations. Whenever a property is accessed the cached
results are returned instead of loading the files again. For more details check
out the `IO docs
<http://api.coala.io/en/latest/Developers/IO.html>`_ .

The NextGen-Core's main caching mechanism is based on task objects. Bears can
offload tasks via `generate_tasks()` which get executed by a Python pool.
Structure wise the cache is a dictionary-like-object with bear types and
cache-tables as key value pairs. The cache-tables themselves are
dictionary-like-objects that map the hash values of the task objects
(generated by ``PersistentHash.persistent_hash``) to the bear results.

At the time of scheduling the bears, the core performs a cache lookup. If the
parameters to ``execute_tasks()`` are the same (in other words it looks for
identical task objects in the cache, and fetches their corresponding results
if found) as that of the previous run then instead of executing that bear again
we get the cached results of that bear.

The NextGen-Core expects the ``analyze`` functions of each bear to provide
results that only depend on the input parameters. In other words ``analyze``
shall be mapping its parameters to results. Using volatile values like
time-dependent data without putting it into the task objects is prohibited since
it might lead to unknown behaviour in coala.
