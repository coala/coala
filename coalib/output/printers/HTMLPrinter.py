from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.printers.HTMLWriter import HTMLWriter

class HTMLPrinter(LogPrinter):
    """
    This is a simple printer/logprinter that prints everything to an HTML file. Note that everything will be appended.
    """
    def __init__(self, filename, log_level=LOG_LEVEL.WARNING, timestamp_format="%X"):
        """
        Creates a new HTMLPrinter. If the directory of the given file doesn't exist or if there's any access problems,
        an exception will be thrown.

        :param filename: the name of the file to put the data into (string).
        """
        self.file = None
        self.log_level = log_level
        if not isinstance(filename, str):
            raise TypeError("filename must be a string.")

        LogPrinter.__init__(self, timestamp_format=timestamp_format, log_level=log_level)
        #self.file = open(filename, 'a+')
        self.htmlwriter = HTMLWriter(filename)
        self.htmlwriter.write_tags

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def _get_log_prefix(self, log_level, timestamp):
        self.log_level = LOG_LEVEL.reverse.get(log_level, "ERROR")

    def _print(self, *args, delimiter=' ', end='\n', color=None, log_date=True):
        if self.log_level == LOG_LEVEL.reverse.get(LOG_LEVEL.WARNING):
            color = "Yellow"
        if self.log_level == LOG_LEVEL.reverse.get(LOG_LEVEL.ERROR):
            color = "Red"
        if self.log_level == LOG_LEVEL.reverse.get(LOG_LEVEL.DEBUG):
            color = "Blue"

        if color is None:
            self.__print_without_color(*args, delimiter=delimiter, end=end)
        else:
            self.__print_with_color(color, *args, delimiter=delimiter, end=end)

    def __print_without_color(self, *args, delimiter, end):
        output = ""
        for arg in args:
            if output != "":
                output += delimiter
            output += arg

        if end == '\n':
            self.htmlwriter.write_tags(p=output)
            return

        self.htmlwriter.write_tags(span=output+end)

    def __print_with_color(self, color, *args, delimiter, end):
        output = ""
        for arg in args:
            if output != "":
                output += delimiter
            output += arg

        if end == '\n':
            self.htmlwriter.write_tag("p", output, style="color:{}".format(color))
            return

        self.htmlwriter.write_tags(span=output+end)
