from functools import total_ordering

from coalib.misc.Decorators import generate_repr


@generate_repr("file", "line")
@total_ordering
class SourcePosition:
    def __init__(self, file=None, line=None):
        """
        Creates a new result position object that represents the position of a
        result in the source code.

        :param file:            The filename or None.
        :param line:            The line in file or None.
        :raises AssertionError: If a line number without a file is provided.
        """
        self.file = file
        self.line = line

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, other):
        assert self.file is not None or other is None
        self._line = other

    def __str__(self):
        return "file: {}, line: {}".format(
            str(repr(self.file)),
            str(self.line))

    def __eq__(self, other):
        return (self.file == other.file and
                self.line == other.line)

    def __lt__(self, other):
        # Show elements without files first
        if (self.file is None) != (other.file is None):
            return self.file is None

        # Now either both file members are None or both are set
        if self.file != other.file:
            return self.file < other.file

        # Show results with a no or lesser line number first
        if (self.line is None) != (other.line is None):
            return self.line is None

        if self.line != other.line:
            return self.line < other.line

        return False


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
