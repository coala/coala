from collections import defaultdict


class CircularDependencyError(Exception):

    def __init__(self, bears):
        """
        Creates the CircularDependencyError with a helpful message about the
        dependency.
        """
        bear_names = (bear.name for bear in bears)
        super(CircularDependencyError, self).__init__(
            "Circular dependency detected: " + " -> ".join(bear_names))


class Dependencies:

    def __init__(self):
        self.dependency_dict = defaultdict(set)
        self.dependency_set = set()

    def _add_dependency(self, bear_instance, dependency):
        self.dependency_dict[bear_instance].add(dependency)
        self.dependency_set.add(dependency)

    def add_bear_dependencies(self, bears):
        """
        Take the full bear list and check it for circular dependencies. Then
        continue to add the dependenies of the bears to the class to be
        resolved later.

        :param bears: List of all bears.
        """
        self.check_circular_dependency(bears)
        for bear_instance in bears:
            for bear in bear_instance.BEAR_DEPS:
                self._add_dependency(bear_instance, bear)

    @classmethod
    def _resolve(cls, bears, resolved_bears, seen):
        for bear in bears:
            if bear in resolved_bears:
                continue

            missing = bear.missing_dependencies(resolved_bears)
            if not missing:
                resolved_bears.append(bear)
                continue

            if bear in seen:
                seen.append(bear)
                raise CircularDependencyError(seen)

            seen.append(bear)
            resolved_bears = cls._resolve(missing, resolved_bears, seen)
            resolved_bears.append(bear)
            seen.remove(bear)  # Already resolved, no candidate for circular dep

        return resolved_bears

    @classmethod
    def check_circular_dependency(cls, bears):
        """
        Collects all dependencies of the given bears. This will also remove
        duplicates.

        :param bears: The given bears. Will not be modified.
        :return:      The new list of bears, sorted so that it can be executed
                      sequentially without dependency issues.
        """
        return cls._resolve(bears, [], [])

    def resolve(self, bear_instance):
        """
        When a bear completes this method is called with the instance of that
        bear. The method deletes this bear from the list of dependencies of
        each bear in the dependency dictionary. It returns the bears which
        have all of its dependencies resolved.

        :param bear_instance: The instance of the bear.
        :return:              Returns a list of bears whose dependencies were
                              all resolved and are ready to be scheduled.
        """
        return_bears = []
        bear_type = type(bear_instance)
        if bear_type in self.dependency_set:
            for bear in self.dependency_dict:
                if bear_type in self.dependency_dict[bear]:
                    self.dependency_dict[bear].remove(bear_type)
                    if not self.dependency_dict[bear]:
                        return_bears.append(bear)
        for bear in return_bears:
            del self.dependency_dict[bear]
        return return_bears
