import re

def unescaped_split(pattern,
                    string,
                    max_split = 0,
                    remove_empty_matches = False):
    """
    Splits the given string by the specified pattern. The return character (\n)
    is not a natural split pattern (if you don't specify it yourself).
    :param pattern:              The pattern that defines where to split.
                                 Providing regexes (and not only fixed strings)
                                 is allowed.
    :param string:               The string to split by the defined pattern.
    :param max_split:            Optional. Defines the number of splits this
                                 function performs. If 0 is provided, unlimited
                                 splits are made. If a number bigger than 0 is
                                 passed, this functions only splits
                                 max_split-times and appends the unprocessed
                                 rest of the string to the result. A negative
                                 number won't perform any splits.
    :param remove_empty_matches: Optional. defines whether empty entries should
                                 be removed from the resulting list.
    :return:                     A list containing the split up strings.
    """

    # Split the string with the built-in function re.split().
    match = re.split(pattern, string, max_split, re.DOTALL)

    # If empty entries shall be removed, apply a filter and recollect all
    # non-empty values with the passed iterator.
    if (remove_empty_matches):
        filtered_match = filter(bool, match)
        match = []
        for item in filtered_match:
            match.append(item)

    return match

def search_for(pattern, string, max_matches = 0, flags = 0):
    """
    Searches for a given pattern in a string max_matches-times.
    :param pattern:     The pattern to search for. Providing regexes (and not
                        only fixed strings) is allowed.
    :param string:      The string to search in.
    :param max_matches: Optional. The maximum number of matches to perform.
    :param flags:       Optional. Additional flags to pass to the regex
                        processor.
    """
    if (max_matches == 0):
        # Use plain re.finditer() to find all matches.
        return re.finditer(pattern, string, flags)
    elif (max_matches > 0):
        # Compile the regex expression to gain performance.
        rxc = re.compile(pattern, flags)
        # The in-string position that indicates the beginning of the regex
        # processing.
        pos = 0

        matches = []
        for x in range(0, max_matches):
            current_match = rxc.search(string, pos)

            if (current_match is None):
                # Break out, no more matches found.
                break
            else:
                # Else, append the found match to the match list.
                matches.append(current_match)
                # Update the in-string position.
                pos = current_match.end()

        return matches
    else:
        # Return the unprocessed string.
        return string

