import os
import platform
import re

from coalib.misc.Decorators import yield_once


def _find_set_end(string, start_index):
    length = len(string)
    closing_index = start_index
    if closing_index < length and string[closing_index] == '!':
        closing_index += 1
    if closing_index < length and string[closing_index] == ']':
        closing_index += 1
    while closing_index < length and string[closing_index] != ']':
        closing_index += 1
    return closing_index


def _position_is_bracketed(string, position):
    """
    Tests whether the char at string[position] is inside a valid pair of
    brackets (and therefore looses its special meaning).
    """
    # allow negative positions and trim too long ones
    position = len(string[:position])

    index, length = 0, len(string)
    while index < position:
        char = string[index]
        index += 1
        if char == '[':
            closing_index = _find_set_end(string, index)
            if closing_index < length:
                if index <= position < closing_index:
                    return True
                index = closing_index + 1
    return False


def _iter_choices(pattern):
    """
    Iterate through each choice of an alternative.
    Basically splitting on '|'s if they are not bracketed
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
    Iterates through all glob patterns that can be obtained by combination of
    all choices for each alternative.
    """
    # Taking the leftmost closing parenthesis and the rightmost opening
    # parenthesis left of it ensures that the delimiters belong together and
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

    if None in (start_pos, end_pos):
        yield pattern
    else:
        # iterate through choices inside of parenthesis (separated by '|'):
        for choice in _iter_choices(pattern[start_pos: end_pos]):
            # put glob expression back together with alternative:
            variant = pattern[:start_pos-1] + choice + pattern[end_pos+1:]

            # iterate through alternatives outside of parenthesis
            # (pattern kann have more alternatives elsewhere)
            for glob_pattern in _iter_alternatives(variant):
                yield glob_pattern


def fnmatch(name, pattern):
    """
    Test whether name matches pattern.

    Glob Syntax:
    '[seq]':         Matches any character in seq. Cannot be empty.
                     Any Special Character looses its special meaning in a set.
    '[!seq]':        Matches any character not in seq. Cannot be empty
                     Any Special Character looses its special meaning in a set.
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


def translate(pattern):
    """
    Translate a shell pattern to a regular expression.
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
            elif platform.system() == 'Windows':
                regex += '[^/\\\\]*'
            # on all other (~Unix-) platforms, '*' matches everything but the
            # filesystem separator, most likely '/'.
            else:
                regex += '[^' + re.escape(os.sep) + ']*'
        elif char == '?':
            regex += '.'
        elif char == '[':
            closing_index = _find_set_end(pattern, index)
            if closing_index >= length:
                regex += '\\['
            else:
                sequence = pattern[index:closing_index].replace('\\', '\\\\')
                index = closing_index+1
                if sequence[0] == '!':
                    sequence = '^' + sequence[1:]
                elif sequence[0] == '^':
                    sequence = '\\' + sequence
                regex = "{}[{}]".format(regex, sequence)
        else:
            regex = regex + re.escape(char)
    return regex + '\\Z(?ms)'


def glob(pattern):
    """
    Return a list of paths matching a pathname pattern.

    Glob Syntax:
    '[seq]':         Matches any character in seq. Cannot be empty.
                     Any Special Character looses its special meaning in a set.
    '[!seq]':        Matches any character not in seq. Cannot be empty
                     Any Special Character looses its special meaning in a set.
    '(seq_a|seq_b)': Matches either sequence_a or sequence_b as a whole.
                     More than two or just one sequence can be given.
    '?':             Matches any single character.
    '*':             Matches everything but os.sep.
    '**':            Matches everything.
    """

    return list(iglob(pattern))


def iglob(pattern):
    """
    Return an iterator which yields the paths matching a pathname pattern.

    Glob Syntax:
    '[seq]':         Matches any character in seq. Cannot be empty.
                     Any Special Character looses its special meaning in a set.
    '[!seq]':        Matches any character not in seq. Cannot be empty
                     Any Special Character looses its special meaning in a set.
    '(seq_a|seq_b)': Matches either sequence_a or sequence_b as a whole.
                     More than two or just one sequence can be given.
    '?':             Matches any single character.
    '*':             Matches everything but os.sep.
    '**':            Matches everything.
    """
    for pat in _iter_alternatives(pattern):
        pat = os.path.expanduser(pat)
        pat = os.path.normcase(pat)
        dirname, basename = os.path.split(pat)
        if not has_wildcard(pat):
            if basename:
                if os.path.exists(pat):  # pragma: nocover
                    yield pat
            else:
                # Patterns ending with a slash should match only directories
                if os.path.isdir(dirname):
                    yield pat
            return

        if not dirname:  # pragma: nocover
            if basename == '**':  # pragma: nocover
                for filename in relativ_recursive_glob(dirname, basename):
                    yield filename
            else:  # pragma: nocover
                for filename in relativ_recursive_glob(dirname, basename):
                    yield filename
            return

        # Prevent an infinite recursion if a drive or UNC path contains
        # wildcard characters (i.e. r'\\?\C:').
        if dirname != pat and has_wildcard(dirname):
            dirs = iglob(dirname)
        else:
            dirs = [dirname]
        if has_wildcard(basename):
            if basename == '**':
                glob_in_dir = relativ_recursive_glob
            else:
                glob_in_dir = relativ_wildcard_glob
        else:
            glob_in_dir = relativ_flat_glob
        for dirname in dirs:
            for name in glob_in_dir(dirname, basename):
                yield os.path.join(dirname, name)


# non recursive glob in dir, accepting wildcards
def relativ_wildcard_glob(dirname, pattern):
    if not dirname:  # pragma: nocover
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


# non recursive glob in dir, accepting only basenames
def relativ_flat_glob(dirname, basename):
    if not basename:  # pragma: nocover
        # `os.path.split()` returns an empty basename for paths ending with a
        # directory separator.  'q*x/' should match only directories.
        if os.path.isdir(dirname):  # pragma: nocover
            return [basename]
    else:
        if os.path.exists(os.path.join(dirname, basename)):  # pragma: nocover
            return [basename]
    return []  # pragma: nocover


# recursive relativ glob, accepting only '**'
def relativ_recursive_glob(dirname, pattern):
    assert pattern == '**'
    if dirname:  # pragma: nocover
        yield pattern[:0]
    for relative_dir in _iter_relative_dirs(dirname):
        yield relative_dir


# recursive relativ listdir
def _iter_relative_dirs(dirname):
    if not dirname:  # pragma: nocover
        dirname = os.curdir
    try:
        files_or_dirs = os.listdir(dirname)
    except os.error:
        return
    for file_or_dir in files_or_dirs:
        yield file_or_dir
        path = os.path.join(dirname, file_or_dir) if dirname else file_or_dir
        for sub_file_or_dir in _iter_relative_dirs(path):
            yield os.path.join(file_or_dir, sub_file_or_dir)


wildcard_check_pattern = re.compile('([*?[])')


def has_wildcard(pattern):
    match = wildcard_check_pattern.search(pattern)
    return match is not None
