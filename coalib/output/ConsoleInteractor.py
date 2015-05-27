try:
    # This import has side effects and is needed to make input() behave nicely
    import readline
except ImportError: # pragma: no cover
    pass

from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.results.RESULT_SEVERITY import (
    RESULT_SEVERITY,
    RESULT_SEVERITY_COLORS)
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.Interactor import Interactor
from coalib.misc.i18n import _
from coalib.settings.Setting import Setting


class ConsoleInteractor(Interactor, ConsolePrinter):
    STR_GET_VAL_FOR_SETTING = _("Please enter a value for the setting \"{}\" "
                                "({}) needed by {}: ")
    STR_LINE_DOESNT_EXIST = _("The line belonging to the following result "
                              "cannot be printed because it refers to a line "
                              "that doesn't seem to exist in the given file.")
    STR_PROJECT_WIDE = _("Project wide:")
    FILE_NAME_COLOR = "blue"
    FILE_LINES_COLOR = "blue"

    def __init__(self,
                 log_printer,
                 pre_padding: int=3,
                 print_colored=True):
        """
        A ConsoleInteractor uses the Console to interact with the user.

        :param log_printer: The LogPrinter to use for logging.
        :param pre_padding: Number of code lines to show before a result as
                            context.
        """
        Interactor.__init__(self, log_printer=log_printer)
        ConsolePrinter.__init__(self, print_colored=print_colored)

        self.pre_padding = pre_padding

    def acquire_settings(self, settings_names_dict):
        if not isinstance(settings_names_dict, dict):
            raise TypeError("The settings_names_dict parameter has to be a "
                            "dictionary.")

        result = {}
        for setting_name, arr in settings_names_dict.items():
            value = self._require_setting(setting_name, arr)
            if value is not None:
                result[setting_name] = value

        return result

    def _require_setting(self, setting_name, arr):
        if not isinstance(arr, list) or len(arr) < 2:
            self.log_printer.log(LOG_LEVEL.WARNING,
                                 _("One of the given settings ({}) is not "
                                   "properly described.").
                                 format(str(setting_name)))

            return None

        if len(arr) == 2:
            needed = arr[1]
        else:
            needed = ", ".join(arr[1:-1]) + _(" and ") + arr[-1]

        return input(self.STR_GET_VAL_FOR_SETTING.format(str(setting_name),
                                                         str(arr[0]),
                                                         needed))

    def _format_line(self, line, real_nr="", sign="|", mod_nr="", symbol="", ):
        return "|{:>4}{}{:>4}|{:1}{}".format(real_nr,
                                             sign,
                                             mod_nr,
                                             symbol,
                                             line.rstrip("\n"))

    def _print_result(self, result):
        self.print(self._format_line(
            "[{sev}] {bear}:".format(
                sev=RESULT_SEVERITY.__str__(result.severity),
                bear=result.origin)),
            color=RESULT_SEVERITY_COLORS[result.severity])
        self.print(*[self._format_line(line)
                     for line in result.message.split("\n")],
                   delimiter="\n")

    def _print_actions(self, actions):
        choice = self._choose_action(actions)

        if choice == 0:
            return None, None

        return self._get_action_info(actions[choice - 1])

    def _choose_action(self, actions):
        self.print(self._format_line(
            _("The following options are applicable to this result:")))

        while True:
            self.print(self._format_line(" 0: " + _("Do nothing.")))
            for i, action in enumerate(actions):
                self.print(self._format_line("{:>2}: {}".format(i + 1,
                                                                action.desc)))

            try:
                line = self._format_line(_("Please enter the number of the "
                                           "action you want to execute. "))
                choice = int(input(line))
                if 0 <= choice <= len(actions):
                    return choice
            except ValueError:
                pass

            self.print(self._format_line(_("Please enter a valid number.")))

    def _print_action_failed(self, action_name, exception):
        self.log_printer.log_exception("Failed to execute the action "
                                       "{}.".format(action_name),
                                       exception)

    def _get_action_info(self, action):
        params = action.non_optional_params

        if self.current_section is None:
            raise ValueError("current_section has to be intializied.")

        for param_name in params:
            if param_name not in self.current_section:
                question = self._format_line(
                    _("Please enter a value for the parameter '{}' ({}): ")
                    .format(param_name, params[param_name][0]))
                self.current_section.append(Setting(param_name,
                                                    input(question)))

        return action.name, self.current_section

    def _print_segregation(self):
        self.print(self._format_line(line="",
                                     real_nr="...",
                                     sign="|",
                                     mod_nr="..."),
                   color=self.FILE_LINES_COLOR)

    def _print_lines(self, file_dict, current_line, result_line, result_file):
        """
        Prints the lines between the current and the result line. If needed
        they will be shortened.
        """
        line_delta = result_line - current_line

        if line_delta > self.pre_padding:
            self._print_segregation()

            for i in range(max(result_line - self.pre_padding, 1),
                           result_line + 1):
                self.print(
                    self._format_line(
                        line=file_dict[result_file][i - 1],
                        real_nr=i,
                        mod_nr=i),
                    color=self.FILE_LINES_COLOR)
        else:
            for i in range(1, line_delta + 1):
                self.print(
                    self._format_line(
                        line=file_dict[result_file][current_line + i - 1],
                        real_nr=current_line + i,
                        mod_nr=current_line + i),
                    color=self.FILE_LINES_COLOR)

    def print_results(self, result_list, file_dict):
        if not isinstance(result_list, list):
            raise TypeError("result_list should be of type list")
        if not isinstance(file_dict, dict):
            raise TypeError("file_dict should be of type dict")

        # We can't use None since we need line 109 be executed if file of first
        # result is None
        current_file = False
        current_line = 0

        for result in sorted(result_list):
            if result.file != current_file:
                if result.file in file_dict or result.file is None:
                    current_file = result.file
                    current_line = 0
                    self.print("\n\n{}".format(current_file
                                               if current_file is not None
                                               else self.STR_PROJECT_WIDE),
                               color=self.FILE_NAME_COLOR)
                else:
                    self.log_printer.warn(_("A result ({}) cannot be printed "
                                            "because it refers to a file that "
                                            "doesn't seem to "
                                            "exist.").format(str(result)))
                    continue

            if result.line_nr is not None:
                if current_file is None:
                    raise AssertionError("A result with a line_nr should also "
                                         "have a file.")
                if result.line_nr < current_line:  # pragma: no cover
                    raise AssertionError("The sorting of the results doesn't "
                                         "work correctly.")
                if len(file_dict[result.file]) < result.line_nr - 1:
                    self.print(self._format_line(
                        line=self.STR_LINE_DOESNT_EXIST))
                else:
                    self._print_lines(file_dict,
                                      current_line,
                                      result.line_nr,
                                      result.file)
                    current_line = result.line_nr

            self.print_result(result, file_dict)

    def _print_section_beginning(self, section):
        self.print(_("Executing section {name}...").format(name=section.name))

    def show_bears(self, bears):
        """
        Presents all bears being used in a stylized manner.

        :param bears: Its a dictionary with bears as keys and list of sections
                      containing those bears as values.
        """
        if not bears:
            self.print(_("No bears to show."))
        else:
            for bear in sorted(bears.keys(),
                               key=lambda bear: bear.__class__.__name__):
                self._show_bear(bear, bears[bear], bear.get_metadata())

    def _show_enumeration(self, title, items, indentation, no_items_text):
        """
        This function takes as input an iterable object (preferably a list or
        a dict). And prints in a stylized format. If the iterable object is
        empty, it prints a specific statement give by the user. An e.g :

        <indentation>Title:
        <indentation> * Item 1
        <indentation> * Item 2

        :param title:         Title of the text to be printed
        :param items:         The iterable object.
        :param indentation:   Number of spaces to indent every line by.
        :param no_items_text: Text printed when iterable object is empty.
        """
        if not items:
            self.print(indentation + no_items_text)
        else:
            self.print(indentation + title)
            if isinstance(items, dict):
                for key, value in items.items():
                    self.print(indentation + " * " + key + ": " + value[0])
            else:
                for item in items:
                    self.print(indentation + " * " + item)
        self.print()

    def _show_bear(self, bear, sections, metadata):
        self.print("{bear}:".format(bear=bear.__name__))
        self.print("  " + metadata.desc + "\n")

        self._show_enumeration(_("Used in:"),
                               sections,
                               "  ",
                               _("No sections."))
        self._show_enumeration(_("Needed Settings:"),
                               metadata.non_optional_params,
                               "  ",
                               _("No needed settings."))
        self._show_enumeration(_("Optional Settings:"),
                               metadata.optional_params,
                               "  ",
                               _("No optional settings."))

    def did_nothing(self):
        self.print(_("No existent section was targeted or enabled. Nothing "
                     "to do."))
