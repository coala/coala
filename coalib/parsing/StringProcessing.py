import re


def search_for(pattern, string, flags=0, max_match=0):
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
    if count <= 0:  # Performance branch
        for elem in iterator:
            yield elem
    else:
        for elem in iterator:
            yield elem
            count -= 1
            if count == 0:
                break


def split(pattern,
          string,
          max_split=0,
          remove_empty_matches=False):
    """
    Splits the given string by the specified pattern. The return character (\n)
    is not a natural split pattern (if you don't specify it yourself).
    This function ignores escape sequences.

    :param pattern:              A regex pattern that defines where to split.
    :param string:               The string to split by the defined pattern.
    :param max_split:            Defines the maximum number of splits. If 0 or
                                 less is provided, the number of splits is not
                                 limited.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the result.
    :return:                     An iterator returning the split up strings.
    """
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
                    remove_empty_matches=False):
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
    :param max_split:            Defines the maximum number of splits. If 0 or
                                 less is provided, the number of splits is not
                                 limited.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the result.
    :return:                     An iterator returning the split up strings.
    """
    # Need to use re.search() since using splitting directly is not possible.
    # We need to match the separator only if the number of escapes is even.
    # The solution is to use look-behind-assertions, but these don't support a
    # variable number of letters (means quantifiers are not usable there). So
    # if we try to match the escape sequences too, they would be replaced,
    # because they are consumed then by the regex. That's not wanted.

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

