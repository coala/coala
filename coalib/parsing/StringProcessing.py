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


def unescaped_split(pattern,
                    string,
                    max_split = 0,
                    remove_empty_matches = False):
    """
    Splits the given string by the specified pattern. The return character (\n)
    is not a natural split pattern (if you don't specify it yourself).
    This function handles escaped split-patterns (and so splits only patterns
    that are unescaped).
    CAUTION: Using the escaped character '\' in the pattern the function can
             return strange results. The backslash can interfere with the
             escaping regex-sequence used internally to split.

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
    # Need to use re.search() since using splitting directly is not possible.
    # We need to match the separator only if the number of escapes is even.
    # The solution is to use lookbehind-assertions, but these don't support a
    # variable number of letters (means quantifiers are not usable there). So
    # if we try to match the escape sequences too, they would be replaced,
    # because they are consumed then by the regex. That's not wanted.
    matches = search_for(r"(.*?)(?<!\\)((?:\\\\)*)(?:" + pattern + r")",
                         string,
                         max_split,
                         re.DOTALL)

    for item in matches:
        concat_string = item.group(1)

        if item.group(2) is not None:
            # Escaped escapes were consumed from the second group, append them
            # too.
            concat_string += item.group(2)

        # If our temporary concatenation string is empty and the
        # remove_empty_matches flag is specified, don't append it to the
        # result.
        if not remove_empty_matches or len(concat_string) != 0:
            yield concat_string

    last_pos = item.end()

    # Append the rest of the string, since it's not in the result list (only
    # matches are captured that have a leading separator).
    if not remove_empty_matches or len(string[last_pos : ]) != 0:
        yield string[last_pos : ]


def search_in_between(begin,
                      end,
                      string,
                      max_matches = 0,
                      remove_empty_matches = False):
    """
    Searches for a string enclosed between a specified begin- and end-sequence.
    Also enclosed \n are put into the result. Doesn't handle escape sequences.
    This function is a generator.

    :param begin:                A regex pattern that defines where to start
                                 matching.
    :param end:                  A regex pattern that defines where to end
                                 matching.
    :param string:               The string where to search in.
    :param max_matches           Defines the maximum number of matches. If 0 is
                                 provided, unlimited matches are made.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the resulting list.
    :raises ValueError:          Raised when a negative number is provided for
                                 max_matches.
    :return:                     An iterator returning the matched strings.
    """

    # Compilation of the begin sequence is needed to get the number of
    # capturing groups in it.
    compiled_begin_pattern = re.compile(begin)

    for item in search_for("(?:" + begin + r")(.*?)(?:" + end + r")",
                           string,
                           max_matches,
                           re.DOTALL):
        # If a user provides a pattern with a matching group (concrete a
        # pattern with a capturing group in parentheses "()"), we need to
        # return the right one. That's why we compiled the begin-sequence
        # before.
        if (not remove_empty_matches or
                len(item.group(compiled_begin_pattern.groups + 1)) != 0):
            yield item.group(compiled_begin_pattern.groups + 1)


def unescaped_search_in_between(begin,
                                end,
                                string,
                                max_matches = 0,
                                remove_empty_matches = False):
    """
    Searches for a string enclosed between a specified begin- and end-sequence.
    Also enclosed \n are put into the result.
    Handles escaped begin- and end-sequences (and so only patterns that are
    unescaped).
    This function is a generator.
    CAUTION: Using the escaped character '\' in the begin- or end-sequences
             the function can return strange results. The backslash can
             interfere with the escaping regex-sequence used internally to
             match the enclosed string.

    :param begin:                The begin-sequence where to start matching.
                                 Providing regexes (and not only fixed strings)
                                 is allowed.
    :param end:                  The end-sequence where to end matching.
                                 Providing regexes (and not only fixed strings)
                                 is allowed.
    :param string:               The string where to search in.
    :param max_matches           Defines the maximum number of matches. If 0 is
                                 provided, unlimited matches are made.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the resulting list.
    :raises ValueError:          Raised when a negative number is provided for
                                 max_matches.
    :return:                     An iterator returning the matched strings.
    """
    # Compilation of the begin sequence is needed to get the number of
    # capturing groups in it.
    compiled_begin_pattern = re.compile(begin)

    for item in search_for(r"(?<!\\)(?:\\\\)*(?:" + begin +
                               r")(.*?)(?<!\\)((?:\\\\)*)(?:" + end + r")",
                           string,
                           max_matches,
                           re.DOTALL):

        # If a user provides a pattern with a matching group (concrete a
        # pattern with a capturing group in parentheses "()"), we need to
        # return the right one. That's why we compiled the begin-sequence
        # before.
        concat_string = item.group(compiled_begin_pattern.groups + 1)

        if item.group(compiled_begin_pattern.groups + 2) is not None:
            # Escaped escapes were consumed from the second group, append them
            # too.
            concat_string += item.group(compiled_begin_pattern.groups + 2)

        # If our temporary concatenation string is empty and the
        # remove_empty_matches flag is specified, don't append it to the
        # result.
        if not remove_empty_matches or len(concat_string) != 0:
            yield concat_string

