from functools import total_ordering

from coalib.misc.Decorators import generate_repr


@generate_repr("file", "line", "column")
@total_ordering
class SourcePosition:
    def __init__(self, file=None, line=None, column=None):
        """
        Creates a new result position object that represents the position of a
        result in the source code.

        :param file:            The filename or None.
        :param line:            The line in file or None, the first line is 1.
        :param column:          The column indicating the character. The first
                                one in a line is 1.
        :raises AssertionError: If a line number without a file is provided.
        """
        self.file = file
        self.line = line
        self.column = column

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, other):
        assert self.file is not None or other is None
        self._line = other

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, other):
        assert self.line is not None or other is None
        self._column = other

    def __str__(self):
        return "file: {}, line: {}, column: {}".format(
            str(repr(self.file)),
            str(self.line),
            str(self.column))

    def __eq__(self, other):
        return (self.file == other.file and
                self.line == other.line and
                self.column == other.column)

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

        # Show results with no or lesser column first
        if (self.column is None) != (other.column is None):
            return self.column is None

        if self.column != other.column:
            return self.column < other.column

        return False
