from os.path import relpath, abspath

from coala_utils.decorators import (
    enforce_signature, generate_ordering, generate_repr, get_public_members)
from coalib.results.TextPosition import TextPosition


@generate_repr('file', 'line', 'column')
@generate_ordering('file', 'line', 'column')
class SourcePosition(TextPosition):

    @enforce_signature
    def __init__(self, file: str, line=None, column=None):
        """
        Creates a new result position object that represents the position of a
        result in the source code.

        :param file:        The filename.
        :param line:        The line in file or None, the first line is 1.
        :param column:      The column indicating the character. The first one
                            in a line is 1.
        :raises TypeError:  Raised when
                            - file is not a string or None.
                            - line or columns are no integers.
        """
        TextPosition.__init__(self, line, column)

        self._file = abspath(file)

    @property
    def file(self):
        return self._file

    def __json__(self, use_relpath=False):
        _dict = get_public_members(self)
        if use_relpath:
            _dict['file'] = relpath(_dict['file'])
        return _dict
