from functools import total_ordering


@total_ordering
class ResultPosition:
    def __init__(self, file=None, line=None):
        """
        Creates a new result position object that represents the position of a
        result in the source code.

        :param file:            The filename or None.
        :param line:            The line in file or None.
        :raises AssertionError: If dumb values are provided, e.g. a line number
                                without a file is meaningless.
        """
        self.file = file
        self.line = line
        assert self.file is not None or self.line is None

    def __str__(self):
        return "file: '{}', line: {}".format(
            str(self.file),
            str(self.line))

    def __repr__(self):
        return self.__str__()

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

        # Show results with a lesser line number first
        return self.line < other.line
