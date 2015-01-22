from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.output.LogPrinter import LogPrinter


class FilePrinter(LogPrinter):
    """
    This is a simple printer/logprinter that prints everything to a file. Note that everything will be appended.
    """
    def __init__(self, filename, log_level=LOG_LEVEL.WARNING, timestamp_format="%X"):
        """
        Creates a new FilePrinter. If the directory of the given file doesn't exist or if there's any access problems,
        an exception will be thrown.

        :param filename: the name of the file to put the data into (string).
        """
        self.file = None
        if not isinstance(filename, str):
            raise TypeError("filename must be a string.")

        LogPrinter.__init__(self, timestamp_format=timestamp_format, log_level=log_level)

        self.file = open(filename, 'a+')

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def _print(self, output, **kwargs):
        self.file.write(output)
