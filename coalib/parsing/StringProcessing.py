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


def split(pattern,
          string,
          max_split = 0,
          remove_empty_matches = False):
    """
    Splits the given string by the specified pattern. The return character (\n)
    is not a natural split pattern (if you don't specify it yourself).
    This function ignores escape sequences.

    :param pattern:              A regex pattern that defines where to split.
    :param string:               The string to split by the defined pattern.
    :param max_split:            Defines the maximum number of splits. If 0 is
                                 provided, unlimited splits are made.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the resulting list.
    :raises ValueError:          Raised when a negative number is provided for
                                 max_split.
    :return:                     An iterator returning the split up strings.
    """
    # re.split() is not usable for this function. It has a bug when using too
    # many capturing groups "()".
    matches = search_for(r"(.*?)(?:" + pattern + r")",
                         string,
                         max_split,
                         re.DOTALL)

    for item in matches:
        if not remove_empty_matches or len(item.group(1)) != 0:
            # Return the first matching group. The pattern from parameter can't
            # change the group order.
            yield item.group(1)

    last_pos = item.end()

    # Append the rest of the string, since it's not in the result list (only
    # matches are captured that have a leading separator).
    if not remove_empty_matches or len(string[last_pos : ]) != 0:
        yield string[last_pos : ]

