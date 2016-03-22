import copy

from coalib.misc.Decorators import (
    enforce_signature, generate_ordering, generate_repr)
from coalib.results.TextPosition import TextPosition


@generate_repr("start", "end")
@generate_ordering("start", "end")
class TextRange:

    @enforce_signature
    def __init__(self, start: TextPosition, end: (TextPosition, None)=None):
        """
        Creates a new TextRange.

        :param start:       A TextPosition indicating the start of the range.
                            Can't be ``None``.
        :param end:         A TextPosition indicating the end of the range. If
                            ``None`` is given, the start object will be used
                            here.
        :raises TypeError:  Raised when
                            - start is no TextPosition or None.
                            - end is no TextPosition.
        :raises ValueError: Raised when end position is smaller than start
                            position, because negative ranges are not allowed.
        """

        self._start = start
        self._end = end or copy.deepcopy(start)

        if self._end < start:
            raise ValueError("End position can't be less than start position.")

    @classmethod
    def from_values(cls,
                    start_line=None,
                    start_column=None,
                    end_line=None,
                    end_column=None):
        """
        Creates a new TextRange.

        :param start_line:   The line number of the start position. The first
                             line is 1.
        :param start_column: The column number of the start position. The first
                             column is 1.
        :param end_line:     The line number of the end position. If this
                             parameter is ``None``, then the end position is set
                             the same like start position and end_column gets
                             ignored.
        :param end_column:   The column number of the end position.
        :return:             A TextRange.
        """
        start = TextPosition(start_line, start_column)
        if end_line is None:
            end = None
        else:
            end = TextPosition(end_line, end_column)

        return cls(start, end)

    @classmethod
    def join(cls, a, b):
        """
        Creates a new TextRange that covers the area of two overlapping ones

        :param a: TextRange (needs to overlap b)
        :param b: TextRange (needs to overlap a)
        :return:  A new TextRange covering the union of the Area of a and b
        """
        if not isinstance(a, cls) or not isinstance(b, cls):
            raise TypeError(
                "only instances of {} can be joined".format(cls.__name__))

        if not a.overlaps(b):
            raise ValueError(
                    "{}s must overlap to be joined".format(cls.__name__))

        return cls(min(a.start, b.start), max(a.end, b.end))

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def overlaps(self, other):
        return self.start <= other.end and self.end >= other.start

    def expand(self, text_lines):
        """
        Passes a new TextRange that covers the same area of a file as this one
        would. All values of None get replaced with absolute values.

        values of None will be interpreted as follows:
        self.start.line is None:   -> 1
        self.start.column is None: -> 1
        self.end.line is None:     -> last line of file
        self.end.column is None:   -> last column of self.end.line

        :param text_lines: File contents of the applicable file
        :return:           TextRange with absolute values
        """
        start_line = self.start.line or 1
        start_column = self.start.column or 1
        end_line = self.end.line or len(text_lines)
        end_column = self.end.column or len(text_lines[end_line - 1])

        return TextRange.from_values(start_line,
                                     start_column,
                                     end_line,
                                     end_column)
