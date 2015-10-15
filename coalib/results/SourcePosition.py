from coalib.misc.Decorators import generate_repr, generate_ordering


@generate_repr("file", "line", "column")
@generate_ordering("file", "line", "column")
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
