from coala_utils.decorators import (
    enforce_signature, generate_ordering, generate_repr)


@generate_repr('line', 'column')
@generate_ordering('line', 'column')
class TextPosition:

    @enforce_signature
    def __init__(self, line: (int, None)=None, column: (int, None)=None):
        """
        Creates a new TextPosition object that represents the position inside
        a string with line/column numbers.

        :param line:        The line in file or None, the first line is 1.
        :param column:      The column indicating the character. The first one
                            in a line is 1.
        :raises TypeError:  Raised when line or columns are no integers.
        :raises ValueError: Raised when a column is set but line is None.
        """
        if line is None and column is not None:
            raise ValueError('A column can only be set if a line is set.')

        self._line = line
        self._column = column

    @property
    def line(self):
        return self._line

    @property
    def column(self):
        return self._column

    def __le__(self, other):
        """
        Test whether ``self`` is behind or equals the other
        ``TextPosition``.

        If the column in a ``TextPosition`` is ``None``, consider
        whole line. If the line in a ``TextPosition`` is ``None``,
        consider whole file.

        :param other: ``TextPosition`` to compare with.
        :return:      Whether this ``TextPosition`` is behind the other
                      one or the same.
        """
        if self.line is None or other.line is None:
            return True
        if self.line == other.line:
            return (True
                    if self.column is None or
                    other.column is None
                    else
                    self.column <= other.column)
        else:
            return self.line < other.line

    def __ge__(self, other):
        """
        Test whether ``self`` is ahead of or equals the
        other ``TextPosition``.

        If the column in a ``TextPosition`` is ``None``, consider
        whole line. If the line in a ``TextPosition`` is ``None``,
        consider whole file.

        :param other: ``TextPosition`` to compare with.
        :return:      Whether this ``TextPosition`` is ahead of the other
                      one or the same.
        """
        if self.line is None or other.line is None:
            return True
        if self.line == other.line:
            return (True
                    if self.column is None or
                    other.column is None
                    else
                    self.column >= other.column)
        else:
            return self.line > other.line
