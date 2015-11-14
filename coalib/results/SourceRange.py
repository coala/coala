from coalib.misc.Decorators import generate_repr, generate_ordering
from coalib.results.SourcePosition import SourcePosition


@generate_repr("start", "end")
@generate_ordering("start", "end")
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

    @classmethod
    def from_values(cls,
                    file,
                    start_line=None,
                    start_column=None,
                    end_line=None,
                    end_column=None):
        start = SourcePosition(file, start_line, start_column)
        if not end_line:
            end = None
        else:
            end = SourcePosition(file, end_line, end_column)

        return cls(start, end)

    @classmethod
    def from_clang_range(cls, range):
        """
        Creates a SourceRange from a clang SourceRange object.

        :param range: A cindex.SourceRange object.
        """
        return cls.from_values(range.start.file.name.decode(),
                               range.start.line,
                               range.start.column,
                               range.end.line,
                               range.end.column)

    @property
    def file(self):
        return self.start.file

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def overlaps(self, other):
        return self.start <= other.end and self.end >= other.start
