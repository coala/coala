from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.Interactor import Interactor
from coalib.misc.i18n import _


class ConsoleInteractor(Interactor, ConsolePrinter):
    STR_GET_VAL_FOR_SETTING = _("Please enter a value for the setting \"{}\" ({}) needed by {}: ")
    STR_LINE_DOESNT_EXIST = _("The line belonging to the following result cannot be printed because it refers to a "
                              "line that doesn't seem to exist in the given file.")
    STR_PROJECT_WIDE = _("Project wide:")

    def __init__(self,
                 pre_padding: int=3,
                 log_printer=ConsolePrinter()):
        """
        A ConsoleInteractor uses the Console to interact with the user.

        :param output: "stdout" or "stderr".
        :param pre_padding: Number of code lines to show before a result as context.
        """
        Interactor.__init__(self, log_printer=log_printer)
        ConsolePrinter.__init__(self)

        self.pre_padding = pre_padding

    def acquire_settings(self, settings_names_dict):
        if not isinstance(settings_names_dict, dict):
            raise TypeError("The settings_names_dict parameter has to be a dictionary.")

        result = {}
        for setting_name, arr in settings_names_dict.items():
            value = self._require_setting(setting_name, arr)
            if value is not None:
                result[setting_name] = value

        return result

    def _require_setting(self, setting_name, arr):
        if not isinstance(arr, list) or len(arr) < 2:
            self.log_printer.log(LOG_LEVEL.WARNING, _("One of the given settings ({}) are not properly "
                                                      "described.").format(str(setting_name)))

            return None

        if len(arr) == 2:
            needed = arr[1]
        else:  # Translators: this is the and that connects the last two items of an enumeration (1st, 2nd AND 3rd)
            needed = ", ".join(arr[1:-1]) + _(" and ") + arr[-1]

        return input(self.STR_GET_VAL_FOR_SETTING.format(str(setting_name),
                                                         str(arr[0]),
                                                         needed))

    def _format_line(self, line, real_nr="", sign="|", mod_nr="", symbol="", ):
        return "|{:>4}{}{:>4}|{:1}{}".format(real_nr, sign, mod_nr, symbol, line.rstrip("\n"))

    def _print_result(self, result):
        message_string_list = "[{sev}] {bear}:\n{msg}".format(sev=RESULT_SEVERITY.__str__(result.severity),
                                                              bear=result.origin,
                                                              msg=result.message).split("\n")

        return self.print("\n".join([self._format_line(line) for line in message_string_list]))

    def _print_actions(self, actions):
        self.print(self._format_line(
            _("The following options are applicable to this result (choose "
              "0 for no action):")))

        choice = self._choose_action(actions)

        if choice == 0:
            return None, None

        return self._get_action_info(actions[choice - 1])

    def _choose_action(self, actions):
        while True:
            for i, action in enumerate(actions):
                self.print(self._format_line("{:>2}: {}".format(i + 1, action.desc)))

            try:
                line = self._format_line(_("Please enter the number of the "
                                           "action you want to execute. "))
                choice = int(input(line))
                if 0 <= choice <= len(actions):
                    return choice
            except ValueError:
                pass

            self.print(self._format_line(_("Please enter a valid number.")))

    def _get_action_info(self, action):
        # Otherwise we have a recursive import
        from coalib.settings.Section import Section
        from coalib.settings.Setting import Setting

        params = action.non_optional_params
        section = Section("")

        for param_name in params:
            question = self._format_line(
                _("Please enter a value for the parameter '{}' ({}): ")
                .format(param_name, params[param_name][0]))
            section.append(Setting(param_name, input(question)))

        return action.name, section

    def _print_segregation(self, n=3):
        self.print("\n".join(self._format_line(line="", sign=".") for i in range(n)))

    def _print_lines(self, file_dict, current_line, result_line, result_file):
        """
        Prints the lines between the current and the result line. If needed they will be shortened.
        """
        line_delta = result_line - current_line

        if line_delta > self.pre_padding:
            self._print_segregation()

            for i in range(max(result_line - self.pre_padding, 1), result_line + 1):
                self.print(self._format_line(line=file_dict[result_file][i - 1],
                                             real_nr=i,
                                             mod_nr=i))
        else:
            for i in range(1, line_delta + 1):
                self.print(self._format_line(line=file_dict[result_file][current_line + i - 1],
                                             real_nr=current_line + i,
                                             mod_nr=current_line + i))

    def print_results(self, result_list, file_dict):
        if not isinstance(result_list, list):
            raise TypeError("result_list should be of type list")
        if not isinstance(file_dict, dict):
            raise TypeError("file_dict should be of type dict")

        current_file = False  # We can't use None since we need line 109 be executed if file of first result is None
        current_line = 0

        for result in sorted(result_list):
            if result.file != current_file:
                if result.file in file_dict or result.file is None:
                    current_file = result.file
                    current_line = 0
                    self.print("\n\n{}".format(current_file if current_file is not None else self.STR_PROJECT_WIDE))
                else:
                    self.log_printer.warn(_("A result ({}) cannot be printed because it refers to a file that doesn't"
                                            " seem to exist.").format(str(result)))
                    continue

            if result.line_nr is not None:
                if current_file is None:
                    raise AssertionError("A result with a line_nr should also have a file.")
                if result.line_nr < current_line:  # pragma: no cover
                    raise AssertionError("The sorting of the results doesn't work correctly.")
                if len(file_dict[result.file]) < result.line_nr - 1:
                    self.print(self._format_line(line=self.STR_LINE_DOESNT_EXIST))
                else:
                    self._print_lines(file_dict, current_line, result.line_nr, result.file)
                    current_line = result.line_nr

            self.print_result(result, file_dict)

    def begin_section(self, name):
        self.print(_("Executing section {name}...").format(name=name))

    def did_nothing(self):
        self.print(_("No existent section was targeted nor enabled. Nothing to"
                     "do."))
