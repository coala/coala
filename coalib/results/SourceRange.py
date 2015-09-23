from functools import total_ordering

from coalib.misc.Decorators import generate_repr
from coalib.results.SourcePosition import SourcePosition


@generate_repr("start", "end")
@total_ordering
class SourceRange:
    def __init__(self, start, end):
        if not isinstance(start, SourcePosition):
            raise TypeError("The start of this SourceRange is not a "
                            "SourcePosition")

        if not isinstance(end, SourcePosition):
            raise TypeError("The end of this SourceRange is not a "
                            "SourcePosition")

        if not start.file == end.file:
            raise ValueError("Start and end of this SourceRange are not"
                             "located in the same file")

        if not end >= start:
            raise ValueError("The Start of this SourceRange lies after it's "
                             "end")

        self.start = start
        self.end = end

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
