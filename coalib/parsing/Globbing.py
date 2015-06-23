from fnmatch import fnmatch as legacy_fnmatch
import os
import platform
import re

from coalib.misc.Decorators import yield_once
from coalib.misc.i18n import N_


def _end_of_set_index(string, start_index):
    """
    Returns the position of the appropriate closing bracket for a glob set in
    string.

    :param string:      Glob string with wildcards
    :param start_index: Index at which the set starts, meaning the position
                        right behind the opening bracket
    :return:            Position of appropriate closing bracket
    """
    length = len(string)
    closing_index = start_index
    if closing_index < length and string[closing_index] == '!':
        closing_index += 1

    if closing_index < length:  # the set cannot be closed by a bracket here
        closing_index += 1

    while closing_index < length and string[closing_index] != ']':
        closing_index += 1

    return closing_index


def _position_is_bracketed(string, position):
    """
    Tests whether the char at string[position] is inside a valid pair of
    brackets (and therefore loses its special meaning)

    :param string:   Glob string with wildcards
    :param position: Position of a char in string
    :return:         Whether or not the char is inside a valid set of brackets
    """
    # allow negative positions and trim too long ones
    position = len(string[:position])

    index, length = 0, len(string)
    while index < position:
        char = string[index]
        index += 1
        if char == '[':
            closing_index = _end_of_set_index(string, index)
            if closing_index < length:
                if index <= position < closing_index:
                    return True
                index = closing_index + 1
            else:
                return False
    return False


def _boundary_of_alternatives_indices(pattern):
    """
    Determines the location of a set of alternatives in a glob pattern.
    Alternatives are defined by a matching set of non-bracketed parentheses.

    :param pattern: Glob pattern with wildcards.
    :return:        Indices of the innermost set of matching non-bracketed
                    parentheses in a tuple. The Index of a missing parenthesis
                    will be passed as None.
    """
    # Taking the leftmost closing parenthesis and the rightmost opening
    # parenthesis left of it ensures that the parentheses belong together and
    # the pattern is parsed correctly from the most nested section outwards.
    end_pos = None
    for match in re.finditer('\\)', pattern):
        if not _position_is_bracketed(pattern, match.start()):
            end_pos = match.start()
            break  # break to get leftmost

    start_pos = None
    for match in re.finditer('\\(', pattern[:end_pos]):
        if not _position_is_bracketed(pattern, match.start()):
            start_pos = match.end()
            # no break to get rightmost

    return start_pos, end_pos


@yield_once
def _iter_choices(pattern):
    """
    Iterate through each choice of an alternative. Splits pattern on '|'s if
    they are not bracketed.

    :param pattern: String of choices separated by '|'s
    :return:        Iterator that yields parts of string separated by
                    non-bracketed '|'s
    """
    start_pos = 0
    split_pos_list = [match.start() for match in re.finditer('\\|', pattern)]
    split_pos_list.append(len(pattern))
    for end_pos in split_pos_list:
        if not _position_is_bracketed(pattern, end_pos):
            yield pattern[start_pos: end_pos]
            start_pos = end_pos + 1


@yield_once
def _iter_alternatives(pattern):
    """
    Iterates through all glob patterns that can be obtaines by combination of
    all choices for each alternative

    :param pattern: Glob pattern with wildcards
    :return:        Iterator that yields all glob patterns without alternatives
                    that can be created from the given pattern containing them.
    """
    start_pos, end_pos = _boundary_of_alternatives_indices(pattern)

    if None in (start_pos, end_pos):
        yield pattern
    else:
        # iterate through choices inside of parenthesis (separated by '|'):
        for choice in _iter_choices(pattern[start_pos: end_pos]):
            # put glob expression back together with alternative:
            variant = pattern[:start_pos-1] + choice + pattern[end_pos+1:]

            # iterate through alternatives outside of parenthesis
            # (pattern can have more alternatives elsewhere)
            for glob_pattern in _iter_alternatives(variant):
                yield glob_pattern


def translate(pattern):
    """
    Translates a pattern into a regular expression.

    :param pattern: Glob pattern with wildcards
    :return:        Regular expression with the same meaning
    """
    index, length = 0, len(pattern)
    regex = ''
    while index < length:
        char = pattern[index]
        index += 1
        if char == '*':
            # '**' matches everything
            if index < length and pattern[index] == '*':
                regex += '.*'
            # on Windows, '*' matches everything but the filesystem
            # separators '/' and '\'.
            elif platform.system() == 'Windows':  # pragma: nocover (Windows)
                regex += '[^/\\\\]*'
            # on all other (~Unix-) platforms, '*' matches everything but the
            # filesystem separator, most likely '/'.
            else:
                regex += '[^' + re.escape(os.sep) + ']*'
        elif char == '?':
            regex += '.'
        elif char == '[':
            closing_index = _end_of_set_index(pattern, index)
            if closing_index >= length:
                regex += '\\['
            else:
                sequence = pattern[index:closing_index].replace('\\', '\\\\')
                index = closing_index+1
                if sequence[0] == '!':
                    sequence = '^' + sequence[1:]
                elif sequence[0] == '^':
                    sequence = '\\' + sequence
                regex += '[' + sequence + ']'
        else:
            regex = regex + re.escape(char)
    return regex + '\\Z(?ms)'


def fnmatch(name, pattern):
    """
    Tests whether name matches pattern

    :param name:    File or directory name
    :param pattern: Glob string with wildcards
    :return:        Boolean: Whether or not name is matched by pattern

    Glob Syntax:
    '[seq]':         Matches any character in seq. Cannot be empty.
                     Any special character looses its special meaning in a set.
   '[!seq]':         Matches any character not in seq. Cannot be empty
                     Any special character looses its special meaning in a set.
    '(seq_a|seq_b)': Matches either sequence_a or sequence_b as a whole.
                     More than two or just one sequence can be given.
    '?':             Matches any single character.
    '*':             Matches everything but os.sep.
    '**':            Matches everything.
    """
    name = os.path.normcase(name)
    for pat in _iter_alternatives(pattern):
        pat = os.path.expanduser(pat)
        pat = os.path.normcase(pat)
        match = re.compile(translate(pat)).match
        if match(name) is not None:
            return True
    return False


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
            # "a(cd)" (first call) yields "ac", then "ad",
            # "b(cd)" (second call) yields "bc" and "bd"
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
                if legacy_fnmatch(file_or_dir, self.pat):
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
