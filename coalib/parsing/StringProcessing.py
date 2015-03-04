import re


def __search_for_generator__(pattern, string, max_matches, flags):
    """
    Searches for a given pattern in a string max_matches-times. This is a
    generator function.

    :param pattern:     A regex pattern that defines what to match.
    :param string:      The string to search in.
    :param max_matches: The maximum number of matches to perform.
    :param flags:       Additional flags to pass to the regex processor.
    :return:            An iterator returning MatchGroup objects.
    """
    # Compile the regex expression to gain performance.
    compiled_pattern = re.compile(pattern, flags)
    pos = 0

    for x in range(0, max_matches):
        current_match = compiled_pattern.search(string, pos)

        if current_match is None or pos > len(string):
            # No more matches found.
            break
        else:
            yield current_match

            if pos == current_match.end():
                # Empty match performed.
                pos += 1
            else:
                pos = current_match.end()


def search_for(pattern, string, max_matches = 0, flags = 0):
    """
    Searches for a given pattern in a string max_matches-times.

    :param pattern:     A regex pattern that defines what to match.
    :param string:      The string to search in.
    :param max_matches: The maximum number of matches to perform.
    :param flags:       Additional flags to pass to the regex processor.
    :raises ValueError: Raised when a negative number is provided for
                        max_matches.
    :return:            An iterator returning MatchGroup objects.
    """
    if max_matches == 0:
        return re.finditer(pattern, string, flags)
    elif max_matches > 0:
        return __search_for_generator__(pattern, string, max_matches, flags)
    else:
        raise ValueError("Provided value for parameter 'max_matches' below "
                         "zero. Negative numbers are not allowed.")

