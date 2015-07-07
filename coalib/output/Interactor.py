import shutil

from coalib.output.printers.Printer import Printer

class Interactor(Printer):
    def __init__(self, log_printer):
        Printer.__init__(self)
        self.log_printer = log_printer
        self.file_diff_dict = {}
        self.current_section = None

    def finalize(self, file_dict):
        """
        To be called after all results are given to the interactor.
        """
        for filename in self.file_diff_dict:
            diff = self.file_diff_dict[filename]
            file_dict[filename] = diff.apply(file_dict[filename])

            # Backup original file, override old backup if needed
            shutil.copy2(filename, filename + ".orig")

            # Write new contents
            with open(filename, mode='w') as file:
                file.writelines(file_dict[filename])

    def begin_section(self, section):
        """
        Will be called before the results for a section come in (via
        print_results).

        :param section: The section that will get executed now.
        """
        self.file_diff_dict = {}
        self.current_section = section
        self._print_section_beginning(section)

    def _print_section_beginning(self, section):
        """
        Will be called after initialization current_section in
        begin_section()

        :param section: The section that will get executed now.
        """
        raise NotImplementedError

    def show_bears(self, bears):
        """
        It presents the bears to the user and information about each bear.

        :param bears: A dictionary containing bears as keys and a list of
                      sections which the bear belongs as the value.
        """
        raise NotImplementedError

    def did_nothing(self):
        """
        Will be called after processing a coafile when nothing had to be done,
        i.e. no section was enabled/targeted.
        """
        raise NotImplementedError
