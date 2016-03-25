import re

from coalib.parsing.StringProcessing import InBetweenMatch
from coalib.parsing.StringProcessing.Filters import limit, trim_empty_matches


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

    return limit(re.finditer(pattern, string, flags), max_match)


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
    :return:          An iterator returning MatchObject's.
    """
    _iter = limit(
        filter(lambda match: not position_is_escaped(string, match.start()),
               search_for(pattern, string, flags, 0, use_regex)),
        max_match)

    for elem in _iter:
        yield elem


def _split(string,
           max_split,
           remove_empty_matches,
           matching_function,
           *args,
           **kwargs):
    """
    Splits a string using a given matching-function that matches the separator.

    This function implements general features needed from the split functions
    in this module (the max-split and remove-empty-matches features).

    :param string:               The string where to split.
    :param max_split:            Defines the maximum number of splits. If 0 or
                                 less is provided, the number of splits is not
                                 limited.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the result.
    :param matching_function:    The matching function. It must return
                                 MatchObject's containing the matched
                                 split-separator.
    :param args:                 Positional arguments to invoke the
                                 matching_function with.
    :param kwargs:               Key-value arguments to invoke the
                                 matching_function with.
    """
    last_end_pos = 0

    for match in matching_function(*args, **kwargs):
        split_string = string[last_end_pos: match.start()]
        last_end_pos = match.end()

        if not remove_empty_matches or len(split_string) != 0:
            yield split_string

            max_split -= 1
            if max_split == 0:
                break  # only reachable when max_split > 0

    # Append the rest of the string.
    if not remove_empty_matches or len(string) > last_end_pos:
        yield string[last_end_pos:]


def split(pattern,
          string,
          max_split=0,
          remove_empty_matches=False,
          use_regex=False):
    """
    Splits the given string by the specified pattern. The return character (\\n)
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
    return _split(string,
                  max_split,
                  remove_empty_matches,
                  search_for,
                  pattern,
                  string,
                  0,
                  0,
                  use_regex)


def unescaped_split(pattern,
                    string,
                    max_split=0,
                    remove_empty_matches=False,
                    use_regex=False):
    """
    Splits the given string by the specified pattern. The return character (\\n)
    is not a natural split pattern (if you don't specify it yourself).
    This function handles escaped split-patterns (and so splits only patterns
    that are unescaped).

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
    return _split(string,
                  max_split,
                  remove_empty_matches,
                  unescaped_search_for,
                  pattern,
                  string,
                  0,
                  0,
                  use_regex)


def search_in_between(begin,
                      end,
                      string,
                      max_matches=0,
                      remove_empty_matches=False,
                      use_regex=False):
    """
    Searches for a string enclosed between a specified begin- and end-sequence.
    Also enclosed \\n are put into the result. Doesn't handle escape sequences.

    :param begin:                A pattern that defines where to start
                                 matching.
    :param end:                  A pattern that defines where to end matching.
    :param string:               The string where to search in.
    :param max_matches:          Defines the maximum number of matches. If 0 or
                                 less is provided, the number of matches is not
                                 limited.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the result. An entry is
                                 considered empty if no inner match was
                                 performed (regardless of matched start and
                                 end patterns).
    :param use_regex:            Specifies whether to treat the begin and end
                                 patterns as regexes or simple strings.
    :return:                     An iterator returning InBetweenMatch objects
                                 that hold information about the matched begin,
                                 inside and end string matched.
    """

    if not use_regex:
        begin = re.escape(begin)
        end = re.escape(end)
        # No need to compile the begin sequence, capturing groups get escaped.
        begin_pattern_groups = 0
    else:
        # Compilation of the begin sequence is needed to get the number of
        # capturing groups in it.
        begin_pattern_groups = re.compile(begin).groups

    # Regex explanation:
    # 1. (begin) A capturing group that matches the begin sequence.
    # 2. (.*?)   Match any char unlimited times, as few times as possible. Save
    #            the match in the second capturing group (`match.group(2)`).
    # 3. (end)   A capturing group that matches the end sequence.
    #            Because the previous group is lazy (matches as few times as
    #            possible) the next occurring end-sequence is matched.
    regex = "(" + begin + ")(.*?)(" + end + ")"

    matches = re.finditer(regex, string, re.DOTALL)

    if remove_empty_matches:
        matches = trim_empty_matches(matches,
                                     (begin_pattern_groups + 2,))

    matches = limit(matches, max_matches)

    for m in matches:
        yield InBetweenMatch.from_values(m.group(1),
                                         m.start(1),
                                         m.group(begin_pattern_groups + 2),
                                         m.start(begin_pattern_groups + 2),
                                         m.group(begin_pattern_groups + 3),
                                         m.start(begin_pattern_groups + 3))


def unescaped_search_in_between(begin,
                                end,
                                string,
                                max_matches=0,
                                remove_empty_matches=False,
                                use_regex=False):
    """
    Searches for a string enclosed between a specified begin- and end-sequence.
    Also enclosed \\n are put into the result.
    Handles escaped begin- and end-sequences (and so only patterns that are
    unescaped).

    .. warning::

        Using the escape character '\\' in the begin- or end-sequences
        the function can return strange results. The backslash can
        interfere with the escaping regex-sequence used internally to
        match the enclosed string.

    :param begin:                A regex pattern that defines where to start
                                 matching.
    :param end:                  A regex pattern that defines where to end
                                 matching.
    :param string:               The string where to search in.
    :param max_matches:          Defines the maximum number of matches. If 0 or
                                 less is provided, the number of matches is not
                                 limited.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the result. An entry is
                                 considered empty if no inner match was
                                 performed (regardless of matched start and
                                 end patterns).
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
        begin_pattern_groups = re.compile(begin).groups

    # Regex explanation:
    # 1. (?<!\\)(?:\\\\)*   Unescapes the following char. The first part of
    #                       this regex is a look-behind assertion. Only match
    #                       the following if no single backslash is before it.
    #                       The second part matches all double backslashes.
    #                       In fact this sequence matches all escapes that
    #                       occur as a multiple of two, means the following
    #                       statement is not escaped.
    # 2. (begin)            A capturing group that matches the begin sequence.
    # 3. (.*?)              Match any char unlimited times, as few times as
    #                       possible. Save the match in the capturing group
    #                       after all capturing groups that can appear in
    #                       'begin'.
    # 4. (?<!\\)((?:\\\\)*) Again the unescaping regex, but now all escape-
    #                       characters get captured.
    # 5. (end)              A capturing group that matches the end sequence.
    #                       Because the 3. group is lazy (matches as few times
    #                       as possible) the next occurring end-sequence is
    #                       matched.
    regex = (r"(?<!\\)(?:\\\\)*(" + begin + r")(.*?)(?<!\\)((?:\\\\)*)(" +
             end + ")")

    matches = re.finditer(regex, string, re.DOTALL)

    if remove_empty_matches:
        matches = trim_empty_matches(matches,
                                     (begin_pattern_groups + 2,
                                      begin_pattern_groups + 3))

    matches = limit(matches, max_matches)

    for m in matches:
        yield InBetweenMatch.from_values(m.group(1),
                                         m.start(1),
                                         m.group(begin_pattern_groups + 2) +
                                         m.group(begin_pattern_groups + 3),
                                         m.start(begin_pattern_groups + 2),
                                         m.group(begin_pattern_groups + 4),
                                         m.start(begin_pattern_groups + 4))


def escape(string, escape_chars, escape_with="\\"):
    """
    Escapes all chars given inside the given string.

    :param string:       The string where to escape characters.
    :param escape_chars: The string or Iterable that contains the characters
                         to escape. Each char inside this string will be
                         escaped in the order given. Duplicate chars are
                         allowed.
    :param escape_with:  The string that should be used as escape sequence.
    :return:             The escaped string.
    """
    for chr in escape_chars:
        string = string.replace(chr, escape_with + chr)

    return string


def convert_to_raw(string, exceptions=""):
    """
    Converts a string to its raw form, converting all backslash to double
    backslash except when the backslash escapes a character given in
    exceptions.

    :param string:     The given string that needs to be converted
    :param exceptions: A list of characters that if escaped with backslash
                       should not be converted to double backslash.
    :return:           Returns the corresponding raw string.
    """
    i = 0
    length = len(string)
    output = ""

    while i < length:
        if (string[i] == '\\' and
                i + 1 < length and string[i + 1] not in exceptions):
            output += "\\"
            # If the next character is a ``\`` then we need to write it now
            # itself since otherwise it will be interpreted as a newly started
            # escape sequence - thereby escaping the character at i + 2,
            # which is unintended behavior
            if string[i + 1] == '\\':
                i += 1
        output += string[i]
        i += 1

    return output


def unescape(string):
    """
    Trimms off all escape characters from the given string.

    :param string: The string to unescape.
    """
    regex = r"\\(.)|\\$"

    return re.sub(regex, lambda m: m.group(1), string, 0, re.DOTALL)


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


def unescaped_rstrip(string):
    """
    Strips whitespaces from the right side of given string that are not
    escaped.

    :param string: The string where to strip whitespaces from.
    :return:       The right-stripped string.
    """
    stripped = string.rstrip()
    if (len(string) > len(stripped) and
            position_is_escaped(stripped, len(string))):
        stripped += string[len(stripped)]
    return stripped


def unescaped_strip(string):
    """
    Strips whitespaces of the given string taking escape characters into
    account.

    :param string: The string where to strip whitespaces from.
    :return:       The stripped string.
    """
    return unescaped_rstrip(string).lstrip()


def _nested_search_in_between(begin, end, string):
    """
    Searches for a string enclosed between a specified begin- and end-sequence.
    Matches infinite times.

    This is a function specifically designed to be invoked from
    ``nested_search_in_between()``.

    :param begin:  A regex pattern that defines where to start matching.
    :param end:    A regex pattern that defines where to end matching.
    :param string: The string where to search in.
    :return:       An iterator returning the matched strings.
    """
    # Regex explanation:
    # 1. (begin) A capturing group that matches the begin sequence.
    # 2. (end)   A capturing group that matches the end sequence. Because the
    #            1st group is lazy (matches as few times as possible) the next
    #            occurring end-sequence is matched.
    # The '|' in the regex matches either the first or the second part.
    regex = "(" + begin + ")|(" + end + ")"

    left_match = None
    nesting_level = 0
    for match in re.finditer(regex, string, re.DOTALL):
        if match.group(1) is not None:
            if nesting_level == 0:
                # Store the match of the first nesting level to be able to
                # return the string until the next fitting end sequence.
                left_match = match
            nesting_level += 1
        else:
            # The second group matched. This is the only alternative if group 1
            # didn't, otherwise no match would be performed. No need to compile
            # the begin and end sequences to get the number of capturing groups
            # in them.
            if nesting_level > 0:
                nesting_level -= 1

            if nesting_level == 0 and left_match != None:
                yield InBetweenMatch.from_values(
                    left_match.group(),
                    left_match.start(),
                    string[left_match.end(): match.start()],
                    left_match.end(),
                    match.group(),
                    match.start())

                left_match = None


def nested_search_in_between(begin,
                             end,
                             string,
                             max_matches=0,
                             remove_empty_matches=False,
                             use_regex=False):
    """
    Searches for a string enclosed between a specified begin- and end-sequence.
    Also enclosed \\n are put into the result. Doesn't handle escape sequences,
    but supports nesting.

    Nested sequences are ignored during the match. Means you get only the first
    nesting level returned. If you want to acquire more levels, just reinvoke
    this function again on the return value.

    Using the same begin- and end-sequence won't match anything.

    :param begin:                A pattern that defines where to start
                                 matching.
    :param end:                  A pattern that defines where to end matching.
    :param string:               The string where to search in.
    :param max_matches:          Defines the maximum number of matches. If 0 or
                                 less is provided, the number of splits is not
                                 limited.
    :param remove_empty_matches: Defines whether empty entries should
                                 be removed from the result. An entry is
                                 considered empty if no inner match was
                                 performed (regardless of matched start and
                                 end patterns).
    :param use_regex:            Specifies whether to treat the begin and end
                                 patterns as regexes or simple strings.
    :return:                     An iterator returning the matched strings.
    """

    if not use_regex:
        begin = re.escape(begin)
        end = re.escape(end)

    strings = _nested_search_in_between(begin, end, string)

    if remove_empty_matches:
        strings = filter(lambda x: str(x.inside) != "", strings)

    return limit(strings, max_matches)
