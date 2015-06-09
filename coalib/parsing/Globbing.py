"""
Several methods to match and collect filenames with glob statements.
Our glob syntax is at follows:

    **      matches everything
    *       matches everything but '/' on Linux, '/' and '\\' on Windows
    ?       matches any single character
    [seq]   matches any character in seq
    [!seq]  matches any char not in seq
    \\      escapes the following character and matches it as is
"""

import os
import platform
import re

from coalib.misc.Decorators import yield_once
from coalib.misc.i18n import N_


def _make_selector(pattern_parts):
    """
    Creates an instance of the selector class that fits the first pattern part.

    :param pattern_parts: List of strings representing a file system path that
                          may contain wildcards
    :return:              Selector class that represents the first pattern part
    :raises ValueError:   If the pattern is invalid. (Error message is marked
                          for translation and can thus be used in the UI.)
    """
    pat = pattern_parts[0]
    child_parts = pattern_parts[1:]
    if pat == '**':
        cls = _RecursiveWildcardSelector
    elif '**' in pat:
        raise ValueError(N_("Invalid pattern: '**' can only be "
                            "an entire path component"))
    elif _is_wildcard_pattern(pat):
        cls = _WildcardSelector
    else:
        cls = _PathSelector
    return cls(pat, child_parts)


def _is_wildcard_pattern(pat):
    """
    Decides whether this pattern needs actual matching using fnmatch, or can
    be looked up directly as part of a path.
    """
    return "*" in pat or "?" in pat or "[" in pat


@yield_once
def _iter_or_combinations(pattern,
                          opening_delimiter="(",
                          closing_delimiter=")",
                          separator="|"):
    """
    A pattern can contain an "or" in the form of (a|b|c). This function will
    iterate through all possible combinations. Nesting is supported
    for "(a(b|c)d|e)" it will yield the patterns "abd", "acd" and "e".

    :param pattern:           A string that may contain an "or" representation
                              following the syntax demonstrated above.
    :param opening_delimiter: Character or sequence thereof that marks the
                              beginning of an "or" representation
    :param closing_delimiter: Character or sequence thereof that marks the
                              end of an "or" representation
    :param separator:         Character or sequence thereof that separates the
                              alternatives
    :returns:                 Iterator that yields the results originating from
                              inserting all possible combinations of
                              alternatives into the pattern.
    :raises ValueError:       If the pattern is invalid. (Error message is
                              marked for translation and can thus be used in
                              the UI.)
    """
    # Taking the leftmost closing delimiter and the rightmost opening delimiter
    # left of it ensures that the delimiters belong together and the pattern is
    # parsed correctly from the most nested section outwards.
    closing_pos = pattern.find(closing_delimiter)
    opening_pos = pattern[:closing_pos].rfind(opening_delimiter)

    if (
            (closing_pos == -1) != (opening_pos == -1) or
            # Special case that gets overlooked because opening_delimiter
            # is only being looked for in pattern[:-1] when closing_pos == -1
            (closing_pos == -1 and pattern.endswith(opening_delimiter))):
        raise ValueError(N_("Parentheses of pattern are not matching"))

    if -1 not in (opening_pos, closing_pos):  # parentheses in pattern
        prefix = pattern[:opening_pos]
        parenthesized = pattern[opening_pos+len(opening_delimiter):closing_pos]
        postfix = pattern[closing_pos+len(closing_delimiter):]
        # This loop iterates through all possible combinations that can be
        # inserted in place of the first innermost pair of parentheses:
        # "(a|b)(c|d)" yields "a", then "b"
        for combination in _iter_or_combinations(parenthesized,
                                                 opening_delimiter,
                                                 closing_delimiter,
                                                 separator):
            new_pattern = prefix + combination + postfix
            # This loop iterates through all possible combinations for the new
            # whole pattern, which has it's first pair of parentheses replaced
            # already:
            # "a(c|d)" (first call) yields "ac", then "ad",
            # "b(c|d)" (second call) yields "bc" and "bd"
            for new_combination in _iter_or_combinations(new_pattern,
                                                         opening_delimiter,
                                                         closing_delimiter,
                                                         separator):
                yield new_combination
    elif separator in pattern:
        for choice in pattern.split(separator):
            yield choice
    else:
        yield pattern


def translate_glob_2_re(pattern):
    """
    Translates a glob pattern to a regular expression.
    """

    index, length = 0, len(pattern)
    regex = ''
    while index < length:

        # note: char is 1 behind index
        char = pattern[index]
        index = index+1

        if char == '*':

            # ** matches everything
            if index < length and pattern[index] == '*':
                regex = regex + '.*'
                index = index + 1

            # * matches everything but '/' and r'\\' on Windows
            elif platform.system() == 'Windows':
                regex = regex + '(?!.*/|.*\\\\\\\\).*'

            # * matches everything but '/' on Linux/Unix
            else:
                regex = regex + '[^/]*'

        # ? matches any single character
        elif char == '?':
            regex = regex + '.'

        # [seq] matches any one of seq and [!seq] matches any one not in seq
        elif char == '[':
            position = index  # index: one after '['
            if position < length and pattern[position] == '!':
                position = position+1
            if position < length and pattern[position] == ']':
                position = position+1  # no seq inside brackets
            while position < length and pattern[position] != ']':
                position = position+1  # position one after closing bracket

            # sequence has no end -> '[' interpreted as single char
            if position >= length:
                regex = regex + '\\['

            # seq = sequence inside brackets
            else:
                seq = pattern[index:position].replace('\\', '\\\\')
                index = position+1
                if seq[0] == '!':
                    seq = '^' + seq[1:]
                elif seq[0] == '^':
                    seq = '\\' + seq
                regex = "{}[{}]".format(regex, seq)

        # the next character is escaped and taken as is
        elif char == '\\':
            char = pattern[index]
            index = index+1
            regex = regex + re.escape(char)

        # usual character
        else:
            regex = regex + re.escape(char)

    # (?ms): flags for re.compile(): m = multi-line, s = dot matches all
    return regex + '\Z(?ms)'


class _Selector:
    """
    Every Selector class has a successor Selector class with the remaining
    pattern parts. Together they represent the glob expression that gets
    evaluated.
    """
    def __init__(self, child_parts):
        self.child_parts = child_parts
        if child_parts:
            self.successor = _make_selector(child_parts)
        else:
            self.successor = _TerminatingSelector()

    def collect(self, path=os.path.abspath(os.curdir)):
        return self._collect(path)

    def _collect(self, paths):
        raise NotImplementedError


class _TerminatingSelector:
    """
    Represents the end of a pattern.
    """
    @staticmethod
    def collect(path):
        yield path


class _PathSelector(_Selector):
    """
    Represents names of files and directories that do not need to be matched
    using fnmatch.
    """
    def __init__(self, path, child_parts):
        self.path = path
        _Selector.__init__(self, child_parts)

    def _collect(self, path):
        extended_path = os.path.join(path, self.path)
        if os.path.exists(extended_path):
            for result in self.successor.collect(extended_path):
                yield result


class _WildcardSelector(_Selector):
    """
    Represents names of files and directories that contain wildcards and need
    to be matched using fnmatch.
    """
    def __init__(self, pat, child_parts):
        self.pat = pat
        _Selector.__init__(self, child_parts)

    def _collect(self, path):
        if os.path.isdir(path):
            for file_or_dir in os.listdir(path):
                if fnmatch(file_or_dir, self.pat):
                    file_or_dir = os.path.join(path, file_or_dir)
                    for result in self.successor.collect(file_or_dir):
                        yield result


class _RecursiveWildcardSelector(_Selector):
    """
    Represents the '**' wildcard.
    """
    def __init__(self, pat, child_parts):
        _Selector.__init__(self, child_parts)

    def _collect(self, path):
        for root, dirs, files in os.walk(path, followlinks=True):
            for result in self.successor.collect(root):
                yield result


def iglob(pattern, files=True, dirs=True):
    """
    Iterate over this subtree and yield all existing files matching the given
    pattern.

    :param pattern:     Unix style glob pattern that matches paths
    :param files:       Whether or not to include files
    :param dirs:        Whether or not to include directories
    :return:            List of all files matching the pattern
    :raises ValueError: If an invalid pattern is found. The exception message
                        is marked for translation, thus can be translated
                        dynamically if needed.
    """
    if pattern == "" or (not files and not dirs):
        raise StopIteration()

    for pat in _iter_or_combinations(pattern):
        # extract drive letter, if possible:
        drive_letter, pat = os.path.splitdrive(pat)
        # "/a/b.py" -> ['', 'a', 'b.py'] or \\a\\b.py -> ['', 'a', 'b.py']
        pattern_parts = pat.split(os.sep)
        # replace first pattern part with absolute path root if empty
        if pat.startswith(os.sep):
            pattern_parts[0] = drive_letter and drive_letter + "\\" or os.sep

        selector = _make_selector(pattern_parts)

        for p in selector.collect():
            if os.path.isfile(p) and files is True:
                yield p
            elif os.path.isdir(p) and dirs is True:
                yield p


def glob(pattern, files=True, dirs=True):
    """
    Iterate over this subtree and return a list of all existing files matching
    the given pattern.

    :param pattern: Unix style glob pattern that matches paths
    :param files:   Whether or not to include files
    :param dirs:    Whether or not to include directories
    :return:        List of all files matching the pattern
    """
    return list(iglob(pattern, files, dirs))


def fnmatch(name, pattern, force_case=False):
    """
    Tests whether name matches the pattern

    :param name:       Filename that is being checked.
    :param pattern:    Pattern that matches the filename.
    :param force_case: If False, name and pattern will be first case-normalized
                       if the operating system requires this.
    :return:           True if name matches the pattern, False otherwise
    """

    if not force_case:
        name = os.path.normcase(name)  # only if OS is case insensitive
        pattern = os.path.normcase(pattern)

    match = re.compile(translate_glob_2_re(pattern)).match

    return match(name) is not None
