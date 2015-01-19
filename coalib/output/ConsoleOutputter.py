"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import sys
from coalib.bears.results.LineResult import Result, RESULT_SEVERITY
from coalib.output.ConsolePrinter import ConsolePrinter
from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.output.Outputter import Outputter
from coalib.misc.i18n import _


class ConsoleOutputter(Outputter, ConsolePrinter):
    STR_GET_VAL_FOR_SETTING = _("Please enter a value for the setting \"{}\" ({}) needed by {}: ")
    STR_LINE_DOESNT_EXIST = _("A the line belonging to the following result cannot be printed because it refers to a "
                              "line that doesn't seem to exist in the given file.")
    STR_PROJECT_WIDE = _("Project wide:")

    def __init__(self,
                 output=sys.stdout,
                 log_level=LOG_LEVEL.WARNING,
                 timestamp_format="%X",
                 pre_padding=3,
                 log_printer=None):
        Outputter.__init__(self)
        ConsolePrinter.__init__(self, output=output, log_level=log_level, timestamp_format=timestamp_format)

        self.pre_padding = pre_padding
        self.log_printer = self if log_printer is None else log_printer

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
            self.log(LOG_LEVEL.WARNING,
                     _("One of the given settings ({}) are not properly described.").format(str(setting_name)))

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
        if not isinstance(result, Result):
            raise TypeError("result has to be a Result descendant.")

        message_string_list = "[{sev}] {bear}:\n{msg}".format(sev=RESULT_SEVERITY.__str__(result.severity),
                                                              bear=result.origin,
                                                              msg=result.message).split("\n")

        return self.print("\n".join([self._format_line(line) for line in message_string_list]))

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

            if hasattr(result, "line_nr"):
                if current_file is None:
                    raise AssertionError("A result with a line_nr should also have a file.")
                if result.line_nr < current_line:  # pragma: no cover
                    raise AssertionError("The sorting of the results doesn't work correctly.")
                if len(file_dict[result.file]) < result.line_nr - 1:
                    self.print(self._format_line(line=self.STR_LINE_DOESNT_EXIST))
                else:
                    self._print_lines(file_dict, current_line, result.line_nr, result.file)
                    current_line = result.line_nr

            self._print_result(result)
