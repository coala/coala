import re

def unescaped_split(pattern,
                    string,
                    max_split = 0,
                    remove_empty_matches = False):
    """
    Splits the given string by the specified pattern.
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
    match = re.split(pattern, string, max_split)

    # If empty entries shall be removed, apply a filter and recollect all
    # non-empty values with the passed iterator.
    if (remove_empty_matches):
        filtered_match = filter(bool, match)
        match = []
        for item in filtered_match:
            match.append(item)

    return match

