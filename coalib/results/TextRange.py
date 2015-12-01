from coalib.misc.Decorators import (enforce_signature,
                                    generate_ordering,
                                    generate_repr)
from coalib.results.TextPosition import TextPosition


@generate_repr("start", "end")
@generate_ordering("start", "end")
class TextRange:
    @enforce_signature
    def __init__(self, start: TextPosition, end: (TextPosition, None)=None):
        """
        Creates a new TextRange.

        :param start:       A TextPosition indicating the start of the range.
                            Can't be `None`.
        :param end:         A TextPosition indicating the end of the range. If
                            `None` is given, the start object will be used
                            here.
        :raises TypeError:  Raised when
                            - start is no TextPosition or None.
                            - end is no TextPosition.
        :raises ValueError: Raised when end position is smaller than start
                            position, because negative ranges are not allowed.
        """

        self._start = start
        self._end = end or start

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
                             parameter is `None`, then the end position is set
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

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end
