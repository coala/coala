from coala_utils.decorators import (
    enforce_signature, generate_ordering, generate_repr, get_public_members)
from coalib.nestedlib.NlSectionPosition import NlSectionPosition
from coalib.results.TextRange import TextRange

@generate_repr('file', 'index', 'language', 'start', 'end', 'linted_start',
               'linted_end')
class NlSection(TextRange):

    @enforce_signature
    def __init__(self,
                 file: str,
                 index: int,
                 language: str,
                 start: NlSectionPosition,
                 end: (NlSectionPosition, None) = None,
                 temp_file=None):
        """
        Create a new NlSection.

        :param start:       A NlSectionPosition indicating the start of the
                            section in original file.
        :param end:         A NlSectionPosition indicating the end of the
                            section in the original file.
                            If ``None`` is given, the start object will be used
                            here. end must be in the same file and be greater
                            than start as negative ranges are not allowed.
        :param language:    The programming language of the lines.
        :param index:       The index of the nl_section.
        :param file:        The name of the original file
        :param temp_file:   The name of the temporary segregated file
        :raises TypeError:  Raised when
                            - start is not of type NlSectionPosition.
                            - end is neither of type NlSectionPosition, nor
                              is it None.
                            - file is not of type str
                            - index is not of type int
                            - language is not of type str
        :raises ValueError: Raised when file of start and end mismatch.
        """
        TextRange.__init__(self, start, end)
        self.index = index
        self.language = language

        """
        :linted_start: The start of the section in the linted file.Initially it
                       is same as that of the start of the original file. It
                       changes only when any patches are applied on that line.
        :linted_end:   The end of the section in the linted file.Initially it
                       is same as that of the end of the original file. It
                       changes only when any patches are applied on that line.
                       If ``None`` is given, the start object will be used
                       here
        """
        self.linted_start = NlSectionPosition(file, start.line, start.column)
        if end:
            self.linted_end = NlSectionPosition(file, end.line, end.column)
        else:
            self.linted_end = NlSectionPosition(file, start.line, start.column)

        if self.start.file != self.end.file:
            raise ValueError('File of start and end position do not match.')

    @classmethod
    def from_values(cls,
                    file,
                    index,
                    language,
                    start_line=None,
                    start_column=None,
                    end_line=None,
                    end_column=None,):
        start = NlSectionPosition(file, start_line, start_column)
        if end_line or (end_column and end_column > start_column):
            end = NlSectionPosition(file, end_line if end_line else start_line,
                                    end_column)
        else:
            end = None
        return cls(file, index, language, start, end)

    @property
    def file(self):
        return self.start.file

    def __str__(self):
        """
        Create a string representation of the NlSection object.

        If the whole file is affected, then just the filename is shown.

        >>> str(NlSection.from_values('test_file', 1, 'html', None, None,
        ... None, None))
        '...test_file: 1: html: '

        If the whole line is affected, then just the filename with starting
        line number and ending line number is shown.

        >> str(NlSection.from_values('test_file', 1, 'html', 1, None, 2, None))
        '...test_file: 1: html: L1: L2: L1: L2'

        This is the general case where particular column and line are
        specified. It shows the starting line and column and ending line
        and column, with filename in the beginning.

        >>> str(NlSection.from_values('test_file', 1, 'html', 1, 1, 2, 1))
        '...test_file: 1: html: L1 C1: L2 C1: L1 C1: L2 C1'
        """
        section_details = '{0.index}: {0.language}: '
        if self.start.line is None and self.end.line is None:
            format_str = '{0.start.file}: ' + section_details
        elif self.start.column is None and self.end.column is None:
            format_str = ('{0.start.file}: ' + section_details +
                          'L{0.start.line}: L{0.end.line}:' +
                          ' L{0.linted_start.line}: L{0.linted_end.line}')
        else:
            format_str = ('{0.start.file}: ' + section_details +
                          'L{0.start.line} C{0.start.column}: ' +
                          'L{0.end.line} C{0.end.column}: ' +
                          'L{0.linted_start.line} C{0.linted_start.column}: '
                          + 'L{0.linted_end.line} C{0.linted_end.column}')

        return format_str.format(self)
