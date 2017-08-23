from coalib.core.CircularDependencyError import CircularDependencyError


def _resolve(bears, resolved_bears, seen):
    for bear in bears:
        if bear in resolved_bears:
            continue

        missing = bear.missing_dependencies(resolved_bears)
        if not missing:
            resolved_bears.append(bear)
            continue

        if bear in seen:
            seen.append(bear)
            raise CircularDependencyError(s.name for s in seen)

        seen.append(bear)
        resolved_bears = _resolve(missing, resolved_bears, seen)
        resolved_bears.append(bear)
        seen.remove(bear)  # Already resolved, no candidate for circular dep

    return resolved_bears


def resolve(bears):
    """
    Collects all dependencies of the given bears. This will also remove
    duplicates.

    :param bears: The given bears. Will not be modified.
    :return:      The new list of bears, sorted so that it can be executed
                  sequentially without dependency issues.
    """
    return _resolve(bears, [], [])
