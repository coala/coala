import re


def search_for(pattern, string, flags = 0, max_match = 0):
    """
    Searches for a given pattern in a string.

    :param pattern:   A regex pattern that defines what to match.
    :param string:    The string to search in.
    :param flags:     Additional flags to pass to the regex processor.
    :param max_match: Defines the maximum number of matches to perform. If 0 or
                      less is provided, the number of splits is not limited.
    :return:          An iterator returning MatchObject's.
    """
    for elem in limit(re.finditer(pattern, string, flags), max_match):
        yield elem


def limit(iterator, count):
    """
    A filter that removes all elements behind the set limit.

    :param iterator: The iterator to be filtered.
    :param count:    The iterator limit. All elements at positions bigger than
                     this limit are trimmed off. Exclusion: 0 or numbers below
                     does not limit at all, means the passed iterator is
                     completely yielded.
    """
    if count <= 0:
        # Use a separate if branch to speed up a bit (since we don't need a
        # counter here).
        for elem in iterator:
            yield elem
    else:
        i = 0
        for elem in iterator:
            yield elem
            i += 1
            if i == count:
                break

