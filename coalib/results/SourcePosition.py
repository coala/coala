from functools import total_ordering

from coalib.misc.Decorators import generate_repr


@generate_repr("file", "line", "column")
@total_ordering
class SourcePosition:
    def __init__(self, file, line=None, column=None):
        """
        Creates a new result position object that represents the position of a
        result in the source code.

        :param file:            The filename or None.
        :param line:            The line in file or None, the first line is 1.
        :param column:          The column indicating the character. The first
                                one in a line is 1.
        :raises AssertionError: If a line number without a file is provided.
        """
        assert isinstance(file, str), "file must be a string!"
        assert isinstance(line, int) or not line, "line must be an int!"
        assert isinstance(column, int) or not column, "column must be an int!"
        assert file is not None or line is None, ("A line must be associated "
                                                  "to a file.")
        assert line is not None or column is None, ("A column can only be set "
                                                    "if a line is set.")

        self._file = file
        self._line = line
        self._column = column

    @property
    def file(self):
        return self._file

    @property
    def line(self):
        return self._line

    @property
    def column(self):
        return self._column

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
