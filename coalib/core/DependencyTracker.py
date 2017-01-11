from itertools import chain

from coalib.core.Graphs import traverse_graph


class DependencyTracker:
    """
    A ``DependencyTracker`` allows to register and manage dependencies between
    objects.

    This class uses a directed graph to track relations.

    Add a dependency relation between two objects:

    >>> object1 = object()
    >>> object2 = object()
    >>> tracker = DependencyTracker()
    >>> tracker.add(object2, object1)

    This would define that ``object1`` is dependent on ``object2``.

    If you define that ``object2`` has its dependency duty fulfilled, you can
    resolve it:

    >>> resolved = tracker.resolve(object2)
    >>> resolved
    {<object object at ...>}
    >>> resolved_object = resolved.pop()
    >>> resolved_object is object1
    True

    This returns all objects that are now freed, meaning they have no
    dependencies any more.

    >>> object3 = object()
    >>> tracker.add(object2, object1)
    >>> tracker.add(object3, object1)
    >>> tracker.resolve(object2)
    set()
    >>> tracker.resolve(object3)
    {<object object at ...>}

    The ones who instantiate a ``DependencyTracker`` are responsible for
    resolving dependencies in the right order. Dependencies which are itself
    dependent will be forcefully resolved and removed from their according
    dependencies too.
    """

    def __init__(self):
        self._dependency_dict = {}

    def get_dependants(self, dependency):
        """
        Returns all immediate dependants for the given dependency.

        >>> tracker = DependencyTracker()
        >>> tracker.add(0, 1)
        >>> tracker.add(0, 2)
        >>> tracker.add(1, 3)
        >>> tracker.get_dependants(0)
        {1, 2}
        >>> tracker.get_dependants(1)
        {3}
        >>> tracker.get_dependants(2)
        set()

        :param dependency:
            The dependency to retrieve all dependants from.
        :return:
            A set of dependants.
        """
        try:
            return set(self._dependency_dict[dependency])
        except KeyError:
            return set()

    def get_dependencies(self, dependant):
        """
        Returns all immediate dependencies of a given dependant.

        >>> tracker = DependencyTracker()
        >>> tracker.add(0, 1)
        >>> tracker.add(0, 2)
        >>> tracker.add(1, 2)
        >>> tracker.get_dependencies(0)
        set()
        >>> tracker.get_dependencies(1)
        {0}
        >>> tracker.get_dependencies(2)
        {0, 1}

        :param dependant:
            The dependant to retrieve all dependencies from.
        :return:
            A set of dependencies.
        """
        return set(
            dependency
            for dependency, dependants in self._dependency_dict.items()
            if dependant in dependants)

    def get_all_dependants(self, dependency):
        """
        Returns a set of all dependants of the given dependency, even
        indirectly related ones.

        >>> tracker = DependencyTracker()
        >>> tracker.add(0, 1)
        >>> tracker.add(1, 2)
        >>> tracker.get_all_dependants(0)
        {1, 2}

        :param dependency:
            The dependency to get all dependants for.
        :return:
            A set of dependants.
        """
        dependants = set()

        def append_to_dependants(prev, nxt):
            dependants.add(nxt)

        traverse_graph(
            [dependency],
            lambda node: self._dependency_dict.get(node, frozenset()),
            append_to_dependants)

        return dependants

    def get_all_dependencies(self, dependant):
        """
        Returns a set of all dependencies of the given dependants, even
        indirectly related ones.

        >>> tracker = DependencyTracker()
        >>> tracker.add(0, 1)
        >>> tracker.add(1, 2)
        >>> tracker.get_all_dependencies(2)
        {0, 1}

        :param dependant:
            The dependant to get all dependencies for.
        :return:
            A set of dependencies.
        """
        dependencies = set()

        def append_to_dependencies(prev, nxt):
            dependencies.add(nxt)

        traverse_graph(
            [dependant],
            lambda node:
                {dependency
                 for dependency, dependants in self._dependency_dict.items()
                 if node in dependants},
            append_to_dependencies)

        return dependencies

    @property
    def dependants(self):
        """
        Returns a set of all registered dependants.

        >>> tracker = DependencyTracker()
        >>> tracker.add(0, 1)
        >>> tracker.add(0, 2)
        >>> tracker.add(1, 3)
        >>> tracker.dependants
        {1, 2, 3}
        """
        return set(chain.from_iterable(self._dependency_dict.values()))

    @property
    def dependencies(self):
        """
        Returns a set of all registered dependencies.

        >>> tracker = DependencyTracker()
        >>> tracker.add(0, 1)
        >>> tracker.add(0, 2)
        >>> tracker.add(1, 3)
        >>> tracker.dependencies
        {0, 1}
        """
        return set(self._dependency_dict.keys())

    def __iter__(self):
        """
        Returns an iterator that iterates over all dependency relations.

        >>> tracker = DependencyTracker()
        >>> tracker.add(0, 1)
        >>> tracker.add(0, 2)
        >>> tracker.add(1, 2)
        >>> for dependency, dependant in sorted(tracker):
        ...     print(dependency, '->', dependant)
        0 -> 1
        0 -> 2
        1 -> 2
        """
        return ((dependency, dependant)
                for dependency, dependants in self._dependency_dict.items()
                for dependant in dependants)

    def add(self, dependency, dependant):
        """
        Add a dependency relation.

        This function does not check for circular dependencies.

        >>> tracker = DependencyTracker()
        >>> tracker.add(0, 1)
        >>> tracker.add(0, 2)
        >>> tracker.resolve(0)
        {1, 2}

        :param dependency:
            The object that is the dependency.
        :param dependant:
            The object that is the dependant.
        """
        if dependency not in self._dependency_dict:
            self._dependency_dict[dependency] = set()

        self._dependency_dict[dependency].add(dependant)

    def resolve(self, dependency):
        """
        Resolves all dependency-relations from the given dependency, and frees
        and returns dependants with no more dependencies. If the given
        dependency is itself a dependant, all those relations are also removed.

        >>> tracker = DependencyTracker()
        >>> tracker.add(0, 1)
        >>> tracker.add(0, 2)
        >>> tracker.add(2, 3)
        >>> tracker.resolve(0)
        {1, 2}
        >>> tracker.resolve(2)
        {3}
        >>> tracker.resolve(2)
        set()

        :param dependency:
            The dependency.
        :return:
            Returns a set of dependants whose dependencies were all resolved.
        """
        # Check if dependency has itself dependencies which aren't resolved,
        # these need to be removed too. This operation does not free any
        # dependencies.
        dependencies_to_remove = []
        for tracked_dependency, dependants in self._dependency_dict.items():
            if dependency in dependants:
                dependants.remove(dependency)

                # If dependants set is now empty, schedule dependency for
                # removal from dependency_dict.
                if not dependants:
                    dependencies_to_remove.append(tracked_dependency)

        for tracked_dependency in dependencies_to_remove:
            del self._dependency_dict[tracked_dependency]

        # Now free dependants which do depend on the given dependency.
        possible_freed_dependants = self._dependency_dict.pop(
            dependency, set())
        non_free_dependants = set()

        for possible_freed_dependant in possible_freed_dependants:
            # Check if all dependencies of dependants from above are satisfied.
            # If so, there are no more dependencies for dependant. Thus it's
            # resolved.
            for dependants in self._dependency_dict.values():
                if possible_freed_dependant in dependants:
                    non_free_dependants.add(possible_freed_dependant)
                    break

        # Remaining dependents are officially resolved.
        return possible_freed_dependants - non_free_dependants

    def check_circular_dependencies(self):
        """
        Checks whether there are circular dependency conflicts.

        >>> tracker = DependencyTracker()
        >>> tracker.add(0, 1)
        >>> tracker.add(1, 0)
        >>> tracker.check_circular_dependencies()
        Traceback (most recent call last):
         ...
        coalib.core.CircularDependencyError.CircularDependencyError: ...

        :raises CircularDependencyError:
            Raised on circular dependency conflicts.
        """
        traverse_graph(
            self._dependency_dict.keys(),
            lambda node: self._dependency_dict.get(node, frozenset()))

    @property
    def are_dependencies_resolved(self):
        """
        Checks whether all dependencies in this ``DependencyTracker`` instance
        are resolved.

        >>> tracker = DependencyTracker()
        >>> tracker.are_dependencies_resolved
        True
        >>> tracker.add(0, 1)
        >>> tracker.are_dependencies_resolved
        False
        >>> tracker.resolve(0)
        {1}
        >>> tracker.are_dependencies_resolved
        True

        :return:
            ``True`` when all dependencies resolved, ``False`` if not.
        """
        return not self._dependency_dict
