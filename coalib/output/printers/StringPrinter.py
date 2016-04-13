from pyprint.Printer import Printer


class StringPrinter(Printer):
    """
    This is a simple printer that prints everything to a string.
    """

    def __init__(self):
        """
        Creates a new StringPrinter with an empty print string.
        """
        Printer.__init__(self)

        self._string = ""

    def _print(self, output, **kwargs):
        self._string += output

    def clear(self):
        """
        Clears the print string.
        """
        self._string = ""

    @property
    def string(self):
        """
        Gets the print string.
        """
        return self._string
