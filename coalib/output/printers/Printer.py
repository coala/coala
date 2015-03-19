class Printer:
    """
    A Printer is an object that can output (usually unformatted) text.

    This object is the base class of every printer and handles output
    concatenation to support the usual delimiter/end parameters. If you want to
    implement a Printer you want to override the _print method which takes just
    one string which is ready to be outputted.

    Examples for some printers are:
    - ConsolePrinter for console and file output
    - EspeakPrinter for Voice output
    - NullPrinter for no output
    """

    def _print(self, output, **kwargs):
        """
        Prints the output parameter. (Will be invoked via the print() method
        while it supports the *args, delimiter and end signature.)

        :param output: A string which shall be printed. (Everything is in it so
                       you don't want to append a newline.)
        :param kwargs: Arbitrary additional keyword arguments which can be used
                       to configure arbitrary things specifically to the
                       printer.
        """
        raise NotImplementedError

    def print(self, *args, delimiter=' ', end='\n', **kwargs):
        """
        Prints the given arguments to an output medium.

        :param args:      Will be outputted.
        :param delimiter: Delimits the args.
        :param end:       Will be appended in the end (without an additional
                          delimiter)
        :param kwargs:    Will be passed through to the Printer derivative
                          handling the actual printing
        """
        output = str(delimiter).join(str(arg) for arg in args) + str(end)

        return self._print(output, **kwargs)
