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
