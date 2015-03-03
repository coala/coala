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

    # re.split() is not usable any more for this function. It has a bug when
    # using too much capturing groups "()". Using the same approach like
    # escaped_split().
    match_strings = []
    matches = search_for(r"(.*?)(?:" + pattern + r")",
                         string,
                         max_split,
                         re.DOTALL)

    # Holds the end position of the last processed and matched string. Needed
    # since matches is a callable_iterator and is not subscriptable, means the
    # last element of the result is not accessible with [] on the fly.
    last_pos = 0
    # Process each returned MatchObject.
    for item in matches:
        if (not remove_empty_matches or len(item.group(1)) != 0):
            # Return the first matching group. The pattern from parameter can't
            # change the group order.
            match_strings.append(item.group(1))

        # Update the end position.
        last_pos = item.end()

    # Append the rest of the string, since it's not in the result list (only
    # matches are captured that have a leading separator).
    if (not remove_empty_matches or len(string[last_pos : ]) != 0):
        match_strings.append(string[last_pos : ])

    return match_strings

def escaped_split(pattern,
                  string,
                  max_split = 0,
                  remove_empty_matches = False):
    """
    Splits the given string by the specified pattern. The return character (\n)
    is not a natural split pattern (if you don't specify it yourself).
    This function handles escaped split-patterns.
    CAUTION: Using the escaped character '\' itself in the pattern the function
             can return strange results. The backslash can interfere with the
             escaping regex-sequence used internally to split.
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

    # Need to use re.search() since using splitting directly is not possible.
    # We need to match the separator only if the number of escapes is even.
    # The solution is to use lookbehind-assertions, but these don't support a
    # variable number of letters (means quantifiers are not usable there). So
    # if we try to match the escape sequences too, they would be replaced,
    # because they are consumed then by the regex. That's not wanted.
    match_strings = []
    matches = search_for(r"(.*?)(?<!\\)((?:\\\\)*)(?:" + pattern + r")",
                         string,
                         max_split,
                         re.DOTALL)

    # Holds the end position of the last processed and matched string. Needed
    # since matches is a callable_iterator and is not subscriptable, means the
    # last element of the result is not accessible with [] on the fly.
    last_pos = 0
    # Process each returned MatchObject.
    for item in matches:
        # Use a temporary concatenation string to check at last if it's empty.
        concat_string = item.group(1)

        if (item.group(2) is not None):
            # If escaped escapes were consumed from the second group, append
            # them too.
            concat_string += item.group(2)

        # If our temporary concatenation string is empty and the
        # remove_empty_matches flag is specified, don't append it to the
        # result.
        if (not remove_empty_matches or len(concat_string) != 0):
            match_strings.append(concat_string)

        # Update the end position.
        last_pos = item.end()

    # Append the rest of the string, since it's not in the result list (only
    # matches are captured that have a leading separator).
    if (not remove_empty_matches or len(string[last_pos : ]) != 0):
        match_strings.append(string[last_pos : ])

    return match_strings

def unescaped_search_in_between(begin,
                                end,
                                string,
                                max_matches = 0,
                                remove_empty_matches = False):
    """
    Searches for a string enclosed between a specified begin- and end-sequence.
    Also enclosed \n are put into the result. Doesn't handle escape sequences.
    :param begin:                The begin-sequence where to start matching.
                                 Providing regexes (and not only fixed strings)
                                 is allowed.
    :param end:                  The end-sequence where to end matching.
                                 Providing regexes (and not only fixed strings)
                                 is allowed.
    :param string:               The string where to search in.
    :param max_matches           Optional. Defines the number of matches this
                                 function performs. If 0 is provided, unlimited
                                 matches are made. If a number bigger than 0 is
                                 passed, this functions only matches
                                 max_matches-times and appends the unprocessed
                                 rest of the string to the result. A negative
                                 number won't perform any matches.
    :param remove_empty_matches: Optional. defines whether empty entries should
                                 be removed from the resulting list.
    :return:                     A list containing the matched strings.
    """

    # Compilation of the begin sequence is needed to get the number of
    # capturing groups in it.
    rxc_begin = re.compile(begin)

    # The found matches are placed inside this variable.
    match_strings = []

    for item in search_for("(?:" + begin + r")(.*?)(?:" + end + r")",
                           string,
                           max_matches,
                           re.DOTALL):
        # If a user provides a pattern with a matching group (concrete a
        # pattern with a capturing group in parantheses "()"), we need to
        # return the right one. That's why we compiled the begin-sequence
        # before.
        if (not remove_empty_matches or
                len(item.group(rxc_begin.groups + 1)) != 0):
            match_strings.append(item.group(rxc_begin.groups + 1))
    return match_strings

def escaped_search_in_between(begin,
                              end,
                              string,
                              max_matches = 0,
                              remove_empty_matches = False):
    """
    Searches for a string enclosed between a specified begin- and end-sequence.
    Also enclosed \n are put into the result.
    Handles escaped begin- and end-sequences.
    CAUTION: Using the escaped character '\' itself in the begin- or
             end-sequences the function can return strange results. The
             backslash can interfere with the escaping regex-sequence used
             internally to match the enclosed string.
    :param begin:                The begin-sequence where to start matching.
                                 Providing regexes (and not only fixed strings)
                                 is allowed.
    :param end:                  The end-sequence where to end matching.
                                 Providing regexes (and not only fixed strings)
                                 is allowed.
    :param string:               The string where to search in.
    :param max_matches           Optional. Defines the number of matches this
                                 function performs. If 0 is provided, unlimited
                                 matches are made. If a number bigger than 0 is
                                 passed, this functions only matches
                                 max_matches-times and appends the unprocessed
                                 rest of the string to the result. A negative
                                 number won't perform any matches.
    :param remove_empty_matches: Optional. defines whether empty entries should
                                 be removed from the resulting list.
    :return:                     A list containing the matched strings.
    """

    # Compilation of the begin sequence is needed to get the number of
    # capturing groups in it.
    rxc_begin = re.compile(begin)

    match_strings = []
    for item in search_for(r"(?<!\\)(?:\\\\)*(?:" + begin +
                               r")(.*?)(?<!\\)((?:\\\\)*)(?:" + end + r")",
                           string,
                           max_matches,
                           re.DOTALL):

        # If a user provides a pattern with a matching group (concrete a
        # pattern with a capturing group in parantheses "()"), we need to
        # return the right one. That's why we compiled the begin-sequence
        # before.
        concat_string = item.group(rxc_begin.groups + 1)

        if (item.group(rxc_begin.groups + 2) is not None):
            # If escaped escapes were consumed from the second group, append
            # them too.
            concat_string += item.group(rxc_begin.groups + 2)

        # If our temporary concatenation string is empty and the
        # remove_empty_matches flag is specified, don't append it to the
        # result.
        if (not remove_empty_matches or len(concat_string) != 0):
            match_strings.append(concat_string)

    return match_strings

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

