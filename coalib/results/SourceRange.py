from os.path import relpath

from coala_utils.decorators import enforce_signature, get_public_members
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
                            - start is not of type SourcePosition.
                            - end is neither of type SourcePosition, nor is it
                              None.
        :raises ValueError: Raised when file of start and end mismatch.
        """
        TextRange.__init__(self, start, end)

        if self.start.file != self.end.file:
            raise ValueError('File of start and end position do not match.')

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

    @enforce_signature
    def affected_source(self, file_dict: dict):
        r"""
        Tells which lines are affected in a specified file within a given range.

        >>> from os.path import abspath
        >>> sr = SourceRange.from_values('file_name', start_line=2, end_line=2)
        >>> sr.affected_source({
        ...     abspath('file_name'): ('def fun():\n', '    x = 2  \n')
        ... })
        ('    x = 2  \n',)

        If more than one line is affected.

        >>> sr = SourceRange.from_values('file_name', start_line=2, end_line=3)
        >>> sr.affected_source({
        ...     abspath('file_name'): ('def fun():\n',
        ...                            '    x = 2  \n', '    print(x)  \n')
        ... })
        ('    x = 2  \n', '    print(x)  \n')

        If the file indicated at the source range is not in the `file_dict` or
        the lines are not given, this will return `None`:

        >>> sr = SourceRange.from_values('file_name_not_present',
        ...     start_line=2, end_line=2)
        >>> sr.affected_source({abspath('file_name'):
        ...     ('def fun():\n', '    x = 2  \n')})

        :param file_dict:
            It is a dictionary where the file names are the keys and
            the contents of the files are the values(which is of type tuple).
        :return:
            A tuple of affected lines in the specified file.
            If the file is not affected or the file is not present in
            ``file_dict`` return ``None``.
        """
        if self.start.file in file_dict and self.start.line and self.end.line:
            # line number starts from 1, index starts from 0
            return file_dict[self.start.file][self.start.line - 1:self.end.line]

    def __json__(self, use_relpath=False):
        _dict = get_public_members(self)
        if use_relpath:
            _dict['file'] = relpath(_dict['file'])
        return _dict

    def __str__(self):
        """
        Creates a string representation of the SourceRange object.

        If the whole file is affected, then just the filename is shown.

        >>> str(SourceRange.from_values('test_file', None, None, None, None))
        '...test_file'

        If the whole line is affected, then just the filename with starting
        line number and ending line number is shown.

        >>> str(SourceRange.from_values('test_file', 1, None, 2, None))
        '...test_file: L1 : L2'

        This is the general case where particular column and line are
        specified. It shows the starting line and column and ending line
        and column, with filename in the beginning.

        >>> str(SourceRange.from_values('test_file', 1, 1, 2, 1))
        '...test_file: L1 C1 : L2 C1'
        """
        if self.start.line is None and self.end.line is None:
            format_str = '{0.start.file}'
        elif self.start.column is None and self.end.column is None:
            format_str = '{0.start.file}: L{0.start.line} : L{0.end.line}'
        else:
            format_str = ('{0.start.file}: L{0.start.line} C{0.start.column}' +
                          ' : L{0.end.line} C{0.end.column}')

        return format_str.format(self)

    def overlaps(self, other):
        return (self.start.file == other.start.file
                and super().overlaps(other))

    def __contains__(self, item):
        return (super().__contains__(item) and
                self.start.file == item.start.file)
