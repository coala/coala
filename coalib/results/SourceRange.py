from os.path import relpath

from coala_decorators.decorators import enforce_signature, get_public_members
from coalib.results.SourcePosition import SourcePosition
from coalib.results.TextRange import TextRange
from coalib.results.AbsolutePosition import AbsolutePosition


class SourceRange(TextRange):

    @enforce_signature
    def __init__(self,
                 start: SourcePosition,
                 end: (SourcePosition, None)=None):
        """
        Creates a new SourceRange.

        :param start:       A SourcePosition indicating the start of the range.
        :param end:         A SourcePosition indicating the end of the range.
                            If ``None`` is given, the start object will be used
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
        if end_line or (end_column and end_column > start_column):
            end = SourcePosition(file, end_line if end_line else start_line,
                                 end_column)
        else:
            end = None

        return cls(start, end)

    @classmethod
    def from_clang_range(cls, range):
        """
        Creates a SourceRange from a clang SourceRange object.

        :param range: A cindex.SourceRange object.
        """
        return cls.from_values(range.start.file.name,
                               range.start.line,
                               range.start.column,
                               range.end.line,
                               range.end.column)

    @classmethod
    @enforce_signature
    def from_absolute_position(cls,
                               file: str,
                               position_start: AbsolutePosition,
                               position_end: (AbsolutePosition, None)=None):
        """
        Creates a SourceRange from a start and end positions.

        :param file:           Name of the file.
        :param position_start: Start of range given by AbsolutePosition.
        :param position_end:   End of range given by AbsolutePosition or None.
        """
        start = SourcePosition(file, position_start.line, position_start.column)
        end = None
        if position_end:
            end = SourcePosition(file, position_end.line, position_end.column)
        return cls(start, end)

    @property
    def file(self):
        return self.start.file

    @enforce_signature
    def renamed_file(self, file_diff_dict: dict):
        """
        Retrieves the filename this source range refers to while taking the
        possible file renamings in the given file_diff_dict into account:

        :param file_diff_dict: A dictionary with filenames as key and their
                               associated Diff objects as values.
        """
        diff = file_diff_dict.get(self.file)
        if diff is None:
            return self.file

        return diff.rename if diff.rename is not False else self.file

    def expand(self, file_contents):
        """
        Passes a new SourceRange that covers the same area of a file as this
        one would. All values of None get replaced with absolute values.

        values of None will be interpreted as follows:
        self.start.line is None:   -> 1
        self.start.column is None: -> 1
        self.end.line is None:     -> last line of file
        self.end.column is None:   -> last column of self.end.line

        :param file_contents: File contents of the applicable file
        :return:              TextRange with absolute values
        """
        tr = TextRange.expand(self, file_contents)

        return SourceRange.from_values(self.file,
                                       tr.start.line,
                                       tr.start.column,
                                       tr.end.line,
                                       tr.end.column)

    def __json__(self, use_relpath=False):
        _dict = get_public_members(self)
        if use_relpath:
            _dict['file'] = relpath(_dict['file'])
        return _dict
