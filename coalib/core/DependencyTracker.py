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
