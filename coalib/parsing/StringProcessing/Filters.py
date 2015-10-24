def limit(iterator, count):
    """
    A filter that removes all elements behind the set limit.

    :param iterator: The iterator to be filtered.
    :param count:    The iterator limit. All elements at positions bigger than
                     this limit are trimmed off. Exclusion: 0 or numbers below
                     does not limit at all, means the passed iterator is
                     completely yielded.
    """
    if count <= 0:  # Performance branch
        for elem in iterator:
            yield elem
    else:
        for elem in iterator:
            yield elem
            count -= 1
            if count == 0:
                break


def trim_empty_matches(iterator, groups=(0,)):
    """
    A filter that removes empty match strings. It can only operate on iterators
    whose elements are of type MatchObject.

    :param iterator: The iterator to be filtered.
    :param groups:   An iteratable defining the groups to check for blankness.
                     Only results are not yielded if all groups of the match
                     are blank.
                     You can not only pass numbers but also strings, if your
                     MatchObject contains named groups.
    """
    for elem in iterator:
        if any(len(elem.group(group)) > 0 for group in groups):
            yield elem
