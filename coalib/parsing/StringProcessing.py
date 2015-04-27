import re


def search_for(pattern, string, flags=0, max_match=0, use_regex=False):
    """
    Searches for a given pattern in a string.

    :param pattern:   A pattern that defines what to match.
    :param string:    The string to search in.
    :param flags:     Additional flags to pass to the regex processor.
    :param max_match: Defines the maximum number of matches to perform. If 0 or
                      less is provided, the number of splits is not limited.
    :param use_regex: Specifies whether to treat the pattern as a regex or
                      simple string.
    :return:          An iterator returning MatchObject's.
    """
    if not use_regex:
        pattern = re.escape(pattern)

    for elem in limit(re.finditer(pattern, string, flags), max_match):
        yield elem


def unescaped_search_for(pattern,
                         string,
                         flags=0,
                         max_match=0,
                         use_regex=False):
    """
    Searches for a given pattern in a string that is not escaped.

    :param pattern:   A pattern that defines what to match unescaped.
    :param string:    The string to search in.
    :param flags:     Additional flags to pass to the regex processor.
    :param max_match: Defines the maximum number of matches to perform. If 0 or
                      less is provided, the number of splits is not limited.
    :param use_regex: Specifies whether to treat the pattern as a regex or
                      simple string.
    :return:          An iterator returning MatchObject's. The MatchObject
                      contains the backslashes preceded by your pattern.
    """
    if not use_regex:
        pattern = re.escape(pattern)

    # Regex explanation:
    # 1. (?<!\\)((?:\\\\)*) Unescaping sequence. Only matches backslashes if
    #                       their count is even.
    # 2. (?:pattern)        A non-capturing group that matches the pattern.
    regex = r"(?<!\\)((?:\\\\)*)(?:" + pattern + r")"

    for elem in search_for(regex, string, flags, max_match, True):
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
    if count <= 0:  # Performance branch
        for elem in iterator:
            yield elem
    else:
        for elem in iterator:
            yield elem
            count -= 1
            if count == 0:
                break


def trim_empty_matches(iterator, groups=[0]):
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
        for group in groups:
            if len(elem.group(group)) != 0:
                yield elem
                continue


def split(pattern,
          string,
          max_split=0,
          remove_empty_matches=False,
          use_regex=False):
    """
    Splits the given string by the specified pattern. The return character (\n)
    is not a natural split pattern (if you don't specify it yourself).
    This function ignores escape sequences.

    :param pattern:              A pattern that defines where to split.
    :param string:               The string to split by the defined pattern.
    :param max_split:            Defines the maximum number of splits. If 0 or
                                 less is provided, the number of splits is not
                                 limited.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the result.
    :param use_regex:            Specifies whether to treat the split pattern
                                 as a regex or simple string.
    :return:                     An iterator returning the split up strings.
    """
    if not use_regex:
        pattern = re.escape(pattern)

    # re.split() is not usable for this function. It has a bug when using too
    # many capturing groups "()".

    # Regex explanation:
    # 1. (.*?)              Match any char unlimited times, as few times as
    #                       possible. Save the match in the first capturing
    #                       group (match.group(1)).
    # 2. (?:pattern)        A non-capturing group that matches the
    #                       split-pattern. Because the first group is lazy
    #                       (matches as few times as possible) the next
    #                       occurring split-sequence is matched.
    regex = r"(.*?)(?:" + pattern + r")"

    item = None
    for item in re.finditer(regex, string, re.DOTALL):
        if not remove_empty_matches or len(item.group(1)) != 0:
            # Return the first matching group. The pattern from parameter can't
            # change the group order.
            yield item.group(1)

            max_split -= 1
            if 0 == max_split:
                break  # only reachable when max_split > 0

    if item is None:
        last_pos = 0
    else:
        last_pos = item.end()

    # Append the rest of the string, since it's not in the result list (only
    # matches are captured that have a leading separator).
    if not remove_empty_matches or len(string) > last_pos:
        yield string[last_pos:]


def unescaped_split(pattern,
                    string,
                    max_split=0,
                    remove_empty_matches=False,
                    use_regex=False):
    """
    Splits the given string by the specified pattern. The return character (\n)
    is not a natural split pattern (if you don't specify it yourself).
    This function handles escaped split-patterns (and so splits only patterns
    that are unescaped).
    CAUTION: Using the escaped character '\' in the pattern the function can
             return strange results. The backslash can interfere with the
             escaping regex-sequence used internally to split.

    :param pattern:              A pattern that defines where to split.
    :param string:               The string to split by the defined pattern.
    :param max_split:            Defines the maximum number of splits. If 0 or
                                 less is provided, the number of splits is not
                                 limited.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the result.
    :param use_regex:            Specifies whether to treat the split pattern
                                 as a regex or simple string.
    :return:                     An iterator returning the split up strings.
    """
    # Need to use re.search() since using splitting directly is not possible.
    # We need to match the separator only if the number of escapes is even.
    # The solution is to use look-behind-assertions, but these don't support a
    # variable number of letters (means quantifiers are not usable there). So
    # if we try to match the escape sequences too, they would be replaced,
    # because they are consumed then by the regex. That's not wanted.

    if not use_regex:
        pattern = re.escape(pattern)

    # Regex explanation:
    # 1. (.*?)              Match any char unlimited times, as few times as
    #                       possible. Save the match in the first capturing
    #                       group (match.group(1)).
    # 2. (?<!\\)((?:\\\\)*) Unescaping sequence. Only matches backslashes if
    #                       their count is even.
    # 3. (?:pattern)        A non-capturing group that matches the
    #                       split-pattern. Because the first group is lazy
    #                       (matches as few times as possible) the next
    #                       occurring split-sequence is matched.
    regex = r"(.*?)(?<!\\)((?:\\\\)*)(?:" + pattern + r")"

    item = None
    for item in re.finditer(regex, string, re.DOTALL):
        concat_string = item.group(1)

        if item.group(2) is not None:
            # Escaped escapes were consumed from the second group, append them
            # too.
            concat_string += item.group(2)

        if not remove_empty_matches or len(concat_string) != 0:
            # Return the first matching group. The pattern from parameter can't
            # change the group order.
            yield concat_string

            max_split -= 1
            if max_split == 0:
                break  # only reachable when max_split > 0

    if item is None:
        last_pos = 0
    else:
        last_pos = item.end()

    # Append the rest of the string, since it's not in the result list (only
    # matches are captured that have a leading separator).
    if not remove_empty_matches or len(string) > last_pos:
        yield string[last_pos:]


def search_in_between(begin,
                      end,
                      string,
                      max_matches=0,
                      remove_empty_matches=False,
                      use_regex=False):
    """
    Searches for a string enclosed between a specified begin- and end-sequence.
    Also enclosed \n are put into the result. Doesn't handle escape sequences.

    :param begin:                A pattern that defines where to start
                                 matching.
    :param end:                  A pattern that defines where to end matching.
    :param string:               The string where to search in.
    :param max_matches           Defines the maximum number of matches. If 0 or
                                 less is provided, the number of matches is not
                                 limited.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the result.
    :param use_regex:            Specifies whether to treat the begin and end
                                 patterns as regexes or simple strings.
    :return:                     An iterator returning the matched strings.
    """

    if not use_regex:
        begin = re.escape(begin)
        end = re.escape(end)
        # No need to compile the begin sequence, capturing groups get escaped.
        begin_pattern_groups = 0
    else:
        # Compilation of the begin sequence is needed to get the number of
        # capturing groups in it.
        compiled_begin_pattern = re.compile(begin)
        begin_pattern_groups = compiled_begin_pattern.groups

    # Regex explanation:
    # 1. (?:begin) A non-capturing group that matches the begin sequence.
    # 2. (.*?)     Match any char unlimited times, as few times as possible.
    #              Save the match in the first capturing group
    #              (match.group(1)).
    # 3. (?:end)   A non-capturing group that matches the end sequence.
    #              Because the previous group is lazy (matches as few times as
    #              possible) the next occurring end-sequence is matched.
    regex = r"(?:" + begin + r")(.*?)(?:" + end + r")"

    matches = re.finditer(regex, string, re.DOTALL)

    if remove_empty_matches:
        matches = trim_empty_matches(matches,
                                     [begin_pattern_groups + 1])

    matches = limit(matches, max_matches)

    for elem in matches:
        yield elem.group(begin_pattern_groups + 1)


def unescaped_search_in_between(begin,
                                end,
                                string,
                                max_matches=0,
                                remove_empty_matches=False,
                                use_regex=False):
    """
    Searches for a string enclosed between a specified begin- and end-sequence.
    Also enclosed \n are put into the result.
    Handles escaped begin- and end-sequences (and so only patterns that are
    unescaped).
    CAUTION: Using the escaped character '\' in the begin- or end-sequences
             the function can return strange results. The backslash can
             interfere with the escaping regex-sequence used internally to
             match the enclosed string.

    :param begin:                A regex pattern that defines where to start
                                 matching.
    :param end:                  A regex pattern that defines where to end
                                 matching.
    :param string:               The string where to search in.
    :param max_matches           Defines the maximum number of matches. If 0 or
                                 less is provided, the number of matches is not
                                 limited.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the result.
    :param use_regex:            Specifies whether to treat the begin and end
                                 patterns as regexes or simple strings.
    :return:                     An iterator returning the matched strings.
    """
    if not use_regex:
        begin = re.escape(begin)
        end = re.escape(end)
        # No need to compile the begin sequence, capturing groups get escaped.
        begin_pattern_groups = 0
    else:
        # Compilation of the begin sequence is needed to get the number of
        # capturing groups in it.
        compiled_begin_pattern = re.compile(begin)
        begin_pattern_groups = compiled_begin_pattern.groups

    # Regex explanation:
    # 1. (?<!\\)(?:\\\\)* Unescapes the following char. The first part of this
    #                     regex is a look-behind assertion. Only match the
    #                     following if no single backslash is before it.
    #                     The second part matches all double backslashes.
    #                     In fact this sequence matches all escapes that occur
    #                     as a multiple of two, means the following statement
    #                     is not escaped.
    # 2. (?:begin)        A non-capturing group that matches the begin
    # 3. (.*?)            sequence. Match any char unlimited times, as few
    #                     times as possible. Save the match in the capturing
    #                     group after all capturing groups that can appear in
    #                     'begin'.
    # 4. (?<!\\)(?:\\\\)* Again the unescaping regex.
    # 5. (?:end)          A non-capturing group that matches the end sequence.
    #                     Because the 3. group is lazy (matches as few times as
    #                     possible) the next occurring end-sequence is matched.
    regex = (r"(?<!\\)(?:\\\\)*(?:" + begin + r")(.*?)(?<!\\)((?:\\\\)*)(?:" +
             end + r")")

    matches = re.finditer(regex, string, re.DOTALL)

    if remove_empty_matches:
        matches = trim_empty_matches(matches,
                                     [begin_pattern_groups + 1,
                                      begin_pattern_groups + 2])

    matches = limit(matches, max_matches)

    for elem in matches:
        yield (elem.group(begin_pattern_groups + 1) +
               elem.group(begin_pattern_groups + 2))


def unescape(string):
    """
    Trimms off all escape characters from the given string.

    :param string: The string to unescape.
    """
    regex = r"\\(.)|\\$"

    def replacement_function(match):
        return match.group(1)

    return re.sub(regex, replacement_function, string, 0, re.DOTALL)


def position_is_escaped(string, position=None):
    """
    Checks whether a char at a specific position of the string is preceded by
    an odd number of backslashes.

    :param string:   Arbitrary string
    :param position: Position of character in string that should be checked
    :return:         True if the character is escaped, False otherwise
    """
    escapes_uneven = False
    # iterate backwards, starting one left of position.
    # Slicing provides a sane default behaviour and prevents IndexErrors
    for i in range(len(string[:position]) - 1, -1, -1):
        if string[i] == '\\':
            escapes_uneven = not escapes_uneven
        else:
            break
    return escapes_uneven
