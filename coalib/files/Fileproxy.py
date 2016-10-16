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

    Note: Other properties can be included later as and when required.

    The equality of the object is checked just based on it's filename.
    """

    def __init__(self, filename):
        """
        Constructs a new fileproxy object.
        :param filename: The name of the file to load.
        """
        self.filename = filename
        with open(self.filename, "r", encoding="utf-8") as filehandle:
            self.content = filehandle.read()
        self.lines = tuple(self.content.splitlines(True))

    def __iter__(self):
        """
        :return: A list of lines of the file to iterate over.
        """
        return iter(self.lines)

    def __hash__(self):
        """
        :return: Only hashes the filename.
        """
        return hash(self.filename)

    def __str__(self):
        """
        :return: A string of contents of the whole file.
        """
        return self.content
