from coalib.output.printers.Printer import Printer

class Interactor(Printer):
    def __init__(self, log_printer):
        Printer.__init__(self)
        self.log_printer = log_printer
        self.file_diff_dict = {}
        self.current_section = None
