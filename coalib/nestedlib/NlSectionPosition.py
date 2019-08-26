from os.path import abspath


from coala_utils.decorators import (
    enforce_signature, generate_ordering, generate_repr, get_public_members)
from coalib.results.TextPosition import TextPosition


@generate_repr('file', 'line', 'column')
@generate_ordering('file', 'line', 'column')
class NlSectionPosition(TextPosition):

    @enforce_signature
    def __init__(self, file: str, line=None, column=None):
        """
        Creates a new NlSection Position object that represents the position of
        a NlSection in the original source code having nested languages.

        :param file:        The filename
        :param line:        The line in the file or None, the first line is 1.
        :param column:      The column indicating the character. The first one
                            in a line is 1.
        :raises TypeError:  Raised when
                            - file is not a string or None
                            - line or column are not integers
        """
        TextPosition.__init__(self, line, column)

        self.filename = file
        self._file = abspath(file)

    # The values of linted_start and linted_end changes during appliaction of
    # a patch. Hence we need a setter method
    @TextPosition.line.setter
    def line(self, value):
        self._line = value

    @TextPosition.column.setter
    def column(self, value):
        self._column = value

    @property
    def file(self):
        return self._file

    def __str__(self):
        source_position = self.filename
        if self.line is not None:
            source_position += ':' + str(self.line)
        if self.column is not None:
            source_position += ':' + str(self.column)
        return source_position
