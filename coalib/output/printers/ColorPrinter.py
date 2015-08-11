from coalib.output.printers.Printer import Printer


class ColorPrinter(Printer):
    """
    Usage:

        p = AnyColorPrinter()
        p.print("some", "output", delimiter=" ", end="", color="green");

    How to implement a color printer:

        Just override the _print_colored() and _print_uncolored method.

        Note that if _print_colored throws an exception, _print_uncolored
        will be invoked.

        Do not override _print() like usual printers do since the ColorPrinter
        class handles this for you.
    """

    def __init__(self, print_colored=None):
        """
        Creates a new ColorPrinter.

        :param print_colored: Can be set to False to use uncolored printing
                              only. If None print colored only when supported.
        """
        Printer.__init__(self)

        self.print_colored = print_colored

    def _print(self, output, **kwargs):
        if (
                kwargs.get("color") is None or
                (self.print_colored is None and
                 not self._are_colors_supported())
                or self.print_colored == False):
            return self._print_uncolored(output, **kwargs)

        try:
            return self._print_colored(output, **kwargs)
        except:
            return self._print_uncolored(output, **kwargs)

    def _print_colored(self, output, color=None, **kwargs):
        """
        Override this! Prints the output colored.

        :param output: The string to print.
        :param color:  The color to print the output in, as a string.
        :param kwargs: Arbitrary additional keyword arguments you might need.
        """
        raise NotImplementedError

    def _print_uncolored(self, output, **kwargs):
        """
        Override this! Prints the output uncolored.

        :param output: The string to print.
        :param kwargs: Arbitrary additional keyword arguments you might need.
        """
        raise NotImplementedError

    @staticmethod
    def _are_colors_supported():
        """
        Returns whether color printing is currently supported or not.

        Override this function to restrict default output behaviour with
        colors.

        By default color printing is supported every time.

        Note: Don't invoke this function statically since it is intended that
        color support may also change during Printer life-cycle.

        :return: True if color printing is supported, False if not.
        """
        return True
