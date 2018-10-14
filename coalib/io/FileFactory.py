import os

from coala_utils.decorators import generate_eq
from cached_property import cached_property


@generate_eq('name', 'timestamp')
class FileFactory:
    """
    The ``FileFactory`` is a class to provide different views on a file.
    It contains the following information about the file:

        * The filename (absolute file path).
        * The modification timestamp of the file.
        * The file in raw format.
        * The file in the form of a string UTF-8 decoded from the raw format.
        * The lines of the file in the form of a tuple.

    Two ``FileFactory`` objects are considered equal if they have the
    same filename and timestamp.

    To initialize a ``FileFactory`` object for a file:

    >>> import os
    >>> import tempfile
    >>> temp = tempfile.NamedTemporaryFile(delete=False)
    >>> temp.write(bytes('This is a test file.', 'UTF-8'))
    20
    >>> temp.close()
    >>> ff = FileFactory(temp.name, newline=False)

    File indices start with zero.
    To retrieve a single line:

    >>> ff.get_line(0)
    'This is a test file.'

    Get all the lines in the file at once:

    >>> ff.lines
    ('This is a test file.',)

    Get the file contents in raw format:

    >>> ff.raw
    b'This is a test file.'

    Get the file as a string:

    >>> ff.string
    'This is a test file.'

    Get the filename:

    >>> ff.name == temp.name
    True

    To conveniently iterate over the lines of a file:

    >>> for line in ff:
    ...     print(line)
    This is a test file.

    >>> os.remove(ff.name)
    """

    def __init__(self, filename, newline=True):
        """
        :param filename:
            The filepath.
        """
        self._filename = os.path.abspath(filename)
        self._timestamp = os.path.getmtime(self._filename)
        self._newline = newline

    def get_line(self, line):
        """
        :param line:
            The line number from which the string is to be retrieved.
            The index starts from zero. An ``IndexError`` is raised if
            the line number provided is out of range.
        :return:
            The retrieved string at the given line number from the file.
        """
        return self.lines[line]

    @cached_property
    def lines(self):
        """
        :return:
            A tuple containing the lines of the file.
        """
        lines = self.string.splitlines()
        if self._newline:
            return tuple(line if line.endswith('\n') else line + '\n'
                         for line in lines)
        else:
            return tuple(lines)

    @cached_property
    def raw(self):
        """
        :return:
            The file contents as a byte sequence.
        """
        with open(self._filename, 'rb') as fp:
            return fp.read()

    @cached_property
    def string(self):
        """
        :return:
            The file contents as a string UTF-8 decoded.
        """
        return self.raw.decode(encoding='utf-8')

    @property
    def name(self):
        """
        :return:
            The absolute filepath.
        """
        return self._filename

    @property
    def timestamp(self):
        """
        :return:
            The last modified timestamp of the file.
        """
        return self._timestamp

    def __iter__(self):
        """
        :return:
            An iterator iterating over all lines in the file.
        """
        return iter(self.lines)
