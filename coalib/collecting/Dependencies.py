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
