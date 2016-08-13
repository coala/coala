from coala_utils.decorators import generate_eq


@generate_eq("filename")
class Fileproxy:
    """
    The file proxy is a wrapper object to wrap every file. The file proxy is an
    object that contains properties about the file currently processed (such as
    the filename). It contains:

        * The filename, this is the starting point for every other attribute.
        * The content of the file as a string.
        * The content of the file, line-splitted.

    The equality of the object is checked just based on its filename.

    To initialize a Fileproxy object for a file:

    >>> fp = Fileproxy("./tests/files/FileproxyTestFiles/testfile.txt")

    Now we can get the filename:

    >>> fp.filename
    './tests/files/FileproxyTestFiles/testfile.txt'

    The number of lines in the file:

    >>> len(fp)
    1

    Iterate through the lines of the file:

    >>> for line in fp:
    ...     print(line)
    Old line
    <BLANKLINE>

    Get contents of the file as a string:

    >>> fp.content
    'Old line\\n'

    Get all lines of the file as a list:
    >>> fp.lines
    ['Old line\\n']
    """

    def __init__(self, filename):
        """
        Constructs a new fileproxy object.

        :param filename: The name of the file to load.
        """
        self.filename = filename
        with open(self.filename, encoding="utf-8") as filehandle:
            self.__lines = tuple(filehandle.readlines())
        self.__linecount = len(self.__lines)

    def __iter__(self):
        """
        :return: A list of lines of the file to iterate over.
        """
        return iter(self.__lines)

    def __hash__(self):
        """
        :return: Only hashes the filename.
        """
        return hash(self.filename)

    @property
    def content(self):
        """
        :return: A string of contents of the whole file.
        """
        return "".join(self.__lines)

    @property
    def lines(self):
        """
        :return: A string of contents of the whole file.
        """
        return list(self.__lines)

    def __len__(self):
        """
        :return: No. of lines in file.
        """
        return self.__linecount
