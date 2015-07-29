from coalib.output.ClosableObject import ClosableObject
from coalib.output.printers.Printer import Printer


class FilePrinter(Printer, ClosableObject):
    """
    This is a simple printer/logprinter that prints everything to a file. Note
    that everything will be appended.
    """
    def __init__(self, filename):
        """
        Creates a new FilePrinter. If the directory of the given file doesn't
        exist or if there's any access problems, an exception will be thrown.

        :param filename: the name of the file to put the data into (string).
        """
        Printer.__init__(self)
        ClosableObject.__init__(self)
        self.file = None
        if not isinstance(filename, str):
            raise TypeError("filename must be a string.")

        self.file = open(filename, 'a+')

    def _close(self):
        if self.file is not None:
            self.file.close()

    def _print(self, output, **kwargs):
        self.file.write(output)
