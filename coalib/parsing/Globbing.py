import os
import platform
import re

from coalib.misc.Decorators import yield_once


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


def _absolute_flat_glob(pattern):
    """
    Glob function for a pattern that do not contain wildcards.

    :pattern: File or directory path
    :return:  Iterator that yields at most one valid file or dir name
    """
    dirname, basename = os.path.split(pattern)

    if basename:
        if os.path.exists(pattern):
            yield pattern
    else:
        # Patterns ending with a slash should match only directories
        if os.path.isdir(dirname):
            yield pattern
    return


def _iter_relative_dirs(dirname):
    """
    Recursively iterates subdirectories of all levels from dirname

    :param dirname: Directory name
    :return:        Iterator that yields files and directory from the given dir
                    and all it's (recursive) subdirectories
    """
    if not dirname:
        dirname = os.curdir
    try:
        files_or_dirs = os.listdir(dirname)
    except os.error:
        return
    for file_or_dir in files_or_dirs:
        yield file_or_dir
        path = os.path.join(dirname, file_or_dir)
        for sub_file_or_dir in _iter_relative_dirs(path):
            yield os.path.join(file_or_dir, sub_file_or_dir)


def relative_wildcard_glob(dirname, pattern):
    """
    Non-recursive glob for one directory. Accepts wildcards.

    :param dirname: Directory name
    :param pattern: Glob pattern with wildcards
    :return:        List of files in the dir of dirname that match the pattern
    """
    if not dirname:
        dirname = os.curdir
    try:
        names = os.listdir(dirname)
    except OSError:
        return []
    result = []
    pattern = os.path.normcase(pattern)
    match = re.compile(translate(pattern)).match
    for name in names:
        if match(os.path.normcase(name)):
            result.append(name)
    return result


def relative_flat_glob(dirname, basename):
    """
    Non-recursive glob for one directory. Does not accept wildcards.

    :param dirname:  Directory name
    :param basename: Basename of a file in dir of dirname
    :return:         List containing Basename if the file exists
    """
    if os.path.exists(os.path.join(dirname, basename)):
        return [basename]
    return[]


def relative_recursive_glob(dirname, pattern):
    """
    Recursive Glob for one directory and all its (nested) subdirectories.
    Accepts only '**' as pattern.

    :param dirname: Directory name
    :param pattern: The recursive wildcard '**'
    :return:        Iterator that yields all the (nested) subdirectories of the
                    given dir
    """
    assert pattern == '**'
    if dirname:
        yield pattern[:0]
    for relative_dir in _iter_relative_dirs(dirname):
        yield relative_dir


wildcard_check_pattern = re.compile('([*?[])')


def has_wildcard(pattern):
    """
    Checks whether pattern has any wildcards.

    :param pattern: Glob pattern that may contain wildcards
    :return:        Boolean: Whether or not there are wildcards in pattern
    """
    match = wildcard_check_pattern.search(pattern)
    return match is not None


def iglob(pattern):
    """
    Iterates all filesystem paths that get matched by the glob pattern.
    Syntax is equal to that of fnmatch.

    :param pattern: Glob pattern with wildcards
    :return:        Iterator that yields all file names that match pattern
    """
    for pat in _iter_alternatives(pattern):
        pat = os.path.expanduser(pat)
        pat = os.path.normcase(pat)
        dirname, basename = os.path.split(pat)
        if not has_wildcard(pat):
            for file in _absolute_flat_glob(pat):
                yield file
            return

        if basename == '**':
            relative_glob_function = relative_recursive_glob
        elif has_wildcard(basename):
            relative_glob_function = relative_wildcard_glob
        else:
            relative_glob_function = relative_flat_glob

        if not dirname:
            for file in relative_glob_function(dirname, basename):
                yield file
            return

        # Prevent an infinite recursion if a drive or UNC path contains
        # wildcard characters (i.e. r'\\?\C:').
        if dirname != pat and has_wildcard(dirname):
            dirs = iglob(dirname)
        else:
            dirs = [dirname]

        for dirname in dirs:
            for name in relative_glob_function(dirname, basename):
                yield os.path.join(dirname, name)


def glob(pattern):
    """
    Iterates all filesystem paths that get matched by the glob pattern.
    Syntax is equal to that of fnmatch.

    :param pattern: Glob pattern with wildcards
    :return:        List of all file names that match pattern
    """
    return list(iglob(pattern))
