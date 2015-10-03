from functools import total_ordering

from coalib.misc.Decorators import generate_repr
from coalib.results.SourcePosition import SourcePosition


@generate_repr("start", "end")
@total_ordering
class SourceRange:
    def __init__(self, start, end):
        assert isinstance(start, SourcePosition)
        assert isinstance(end, SourcePosition)

        self.start = start
        self.end = end

    def __eq__(self, other):
        assert isinstance(other, SourceRange)
        return self.start == other.start and self.end == other.end

    def __lt__(self, other):
        assert isinstance(other, SourceRange)

        if self.start != other.start:
            return self.start < other.start

        return self.end < other.end
