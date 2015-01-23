from coalib.output.printers.Printer import Printer


class ColorPrinter(Printer):
    """
    Just use
    p = AnyColorPrinter()
    p.print("some", "output", delimiter=" ", end="", color="green");
    """

    def __init__(self):
        Printer.__init__(self)

    def _print(self, output, **kwargs):
        if kwargs.get("color") is None:
            return self._print_uncolored(output, **kwargs)

        try:
            return self._print_colored(output, **kwargs)
        except:
            return self._print_uncolored(output, **kwargs)

    def _print_colored(self, output, color=None, **kwargs):
        raise NotImplementedError

    def _print_uncolored(self, output, **kwargs):
        raise NotImplementedError
