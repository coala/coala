from coalib.output.printers.Printer import Printer

class Interactor(Printer):
    def __init__(self, log_printer):
        Printer.__init__(self)
        self.log_printer = log_printer
        self.file_diff_dict = {}
        self.current_section = None

    def show_bears(self, bears):
        """
        It presents the bears to the user and information about each bear.

        :param bears: A dictionary containing bears as keys and a list of
                      sections which the bear belongs as the value.
        """
        raise NotImplementedError
