import fnmatch
import os


def _make_selector(pattern_parts):
    pat = pattern_parts[0]
    child_parts = pattern_parts[1:]
    if pat == '**':
        cls = _RecursiveWildcardSelector
    elif '**' in pat:
        raise ValueError("Invalid pattern: '**' can only be "
                         "an entire path component")
    elif _is_wildcard_pattern(pat):
        cls = _WildcardSelector
    else:
        cls = _PathSelector
    return cls(pat, child_parts)


def _is_wildcard_pattern(pat):
    """
    Whether this pattern needs actual matching using fnmatch, or can
    be looked up directly as part of a path.
    """
    return "*" in pat or "?" in pat or "[" in pat


class _Selector:
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
    represents the end of a pattern.
    """
    def collect(self, path):
        yield path


class _PathSelector(_Selector):
    """
    represents names of files and directories that do not need to be matched
    using fnmatch
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
    represents names of files and directories that contain wildcards and need
    to be matched using fnmatch
    """
    def __init__(self, pat, child_parts):
        self.pat = pat
        _Selector.__init__(self, child_parts)

    def _collect(self, path):
        if os.path.isdir(path):
            for file_or_dir in os.listdir(path):
                if fnmatch.fnmatch(file_or_dir, self.pat):
                    file_or_dir = os.path.join(path, file_or_dir)
                    for result in self.successor.collect(file_or_dir):
                        yield result


class _RecursiveWildcardSelector(_Selector):
    """
    represents the '**' wildcard
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

    :param pattern: Unix style glob pattern that matches paths
    :param files: Whether or not to include files
    :param dirs: Whether or not to include directories
    :return: list of all files matching the pattern
    """
    if pattern == "" or (not files and not dirs):
        raise StopIteration()

    pattern_parts = pattern.split(os.sep)  # "/a/b.py" -> ['', 'a', 'b.py']
    if pattern.startswith(os.sep):
        pattern_parts[0] = os.sep  # would be '' instead
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
    :param files: Whether or not to include files
    :param dirs: Whether or not to include directories
    :return: list of all files matching the pattern
    """
    return list(iglob(pattern, files, dirs))
