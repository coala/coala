from functools import total_ordering

from coalib.misc.Decorators import generate_repr
from coalib.results.SourcePosition import SourcePosition


@generate_repr("start", "end")
@total_ordering
class SourceRange:
    def __init__(self, start, end=None):
        """
        Creates a new SourceRange.

        :param start: A SourcePosition indicating the start of the range.
        :param end:   A SourcePosition indicating the end of the range. If
                      `None` is given, the start object will be used here. end
                      must be in the same file and be greater than start as
                      negative ranges are not allowed.
        """
        assert isinstance(start, SourcePosition)

        self._start = start
        if end is None:
            self._end = self.start
        else:
            assert isinstance(end, SourcePosition)
            assert self.start.file == end.file
            assert end >= self.start

            self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def __eq__(self, other):
        if not isinstance(other, SourceRange):
            return False

        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        if not isinstance(other, SourceRange):
            raise TypeError("Cannot compare SourceRange with a variable of"
                            "another type")

        if self.start != other.start:
            return self.start < other.start

        return self.end < other.end
