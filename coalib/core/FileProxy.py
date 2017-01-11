import logging

from coala_utils.decorators import generate_eq


@generate_eq('filename')
class FileProxy:
    """
    The ``FileProxy`` is responsible for providing contents of a file which is
    currently processed by coala. It contains:

    - The filename.
    - The content of the file as a string.
    - The content of the file, line-splitted (including return characters).

    To initialize a ``FileProxy`` object:

    >>> fp = FileProxy(__file__)

    Now we can get the filename:

    >>> fp.filename  # +ELLIPSIS
    '...FileProxy.py'

    Iterate through the lines of the file:

    >>> for line in fp.lines:  # +ELLIPSIS
    ...     print(line)
    from ...

    The ``lines`` iterator supports ``len``.

    Get contents of the file as a string:

    >>> fp.content
    'from ...'

    ``FileProxy`` objects referring to the same file are considered equal:

    >>> fp1 = FileProxy(__file__)
    >>> fp2 = FileProxy(__file__)
    >>> fp1 == fp2
    True
    """

    def __init__(self, filename):
        """
        Constructs a new ``FileProxy`` object.

        :raises UnicodeDecodeError:
            Raised when non-unicode characters appear in the
        :raises OSError:
        :param filename: The name of the file to load.
        """
        self._filename = filename

        try:
            with open(filename, encoding='utf-8') as fl:
                self._content = fl.read()
        except UnicodeDecodeError:
            logging.warning("Failed to read file '{}'. It seems to contain "
                            'non-unicode characters. Leaving it '
                            'out.'.format(filename), )
        except OSError as exception:  # pragma: no cover
            logging.warning("Failed to read file '{}' because of an unknown "
                            'error. Leaving it out.'.format(filename),
                            exc_info=exception)

        self._lines = tuple(self._content.splitlines(True))

    @property
    def filename(self):
        """
        The backing filename.
        """
        return self._filename

    def __hash__(self):
        """
        >>> fp = FileProxy(__file__)
        >>> hash(fp) == hash(__file__)
        True
        """
        return hash(self.filename)

    @property
    def content(self):
        """
        :return: A string containing the whole content of the file.
        """
        return self._content

    @property
    def lines(self):
        """
        :return: An iterable of all lines of the file which supports ``len``.
        """
        return self._lines
