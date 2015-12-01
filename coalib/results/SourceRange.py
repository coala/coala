from coalib.misc.Decorators import enforce_signature
from coalib.results.SourcePosition import SourcePosition
from coalib.results.TextRange import TextRange


class SourceRange(TextRange):
    @enforce_signature
    def __init__(self,
                 start: SourcePosition,
                 end: (SourcePosition, None)=None):
        """
        Creates a new SourceRange.

        :param start:       A SourcePosition indicating the start of the range.
        :param end:         A SourcePosition indicating the end of the range.
                            If `None` is given, the start object will be used
                            here. end must be in the same file and be greater
                            than start as negative ranges are not allowed.
        :raises TypeError:  Raised when
                            - start is no SourcePosition or None.
                            - end is no SourcePosition.
        :raises ValueError: Raised when file of start and end mismatch.
        """
        TextRange.__init__(self, start, end)

        if self.start.file != self.end.file:
            raise ValueError("File of start and end position do not match.")

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

    def overlaps(self, other):
        return self.start <= other.end and self.end >= other.start
