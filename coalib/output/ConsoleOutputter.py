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
    def __init__(self, output=sys.stdout):
        Outputter.__init__(self)
        ConsolePrinter.__init__(self, output=output)

    def acquire_settings(self, settings_names_dict):
        if not isinstance(settings_names_dict, dict):
            raise TypeError("The settings parameter has to be a dictionary.")

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

        return input(_("Please enter a value for the setting \"{}\" ({}) needed by {}: ").format(str(setting_name),
                                                                                                 str(arr[0]),
                                                                                                 needed))

    def _print_result(self, result):
        assert (isinstance(result, Result))
        if result.file is None:
            return self.print(("[{sev}] " + _("Message from {bear}:") +
                               "\n{message}").format(sev=RESULT_SEVERITY.__str__(result.severity),
                                                     bear=result.origin,
                                                     message=result.message))

        return self.print(("[{sev}] " + _("Annotation for file {file} from {bear}:") +
                           "\n{message}").format(sev=RESULT_SEVERITY.__str__(result.severity),
                                                 file=result.file,
                                                 bear=result.origin,
                                                 message=result.message))

    def print_results(self, result_list, file_dict, padding_before=3, padding_after=3):
        """
        Prints all given results. They will be sorted.

        :param result_list: List of the results
        :param file_dict: Dictionary containing filename: file_contents
        """
        # TODO: DOES NOT YET USE A DAMN LINE PRINT FUNCTION
        # todo: also not tested
        if not isinstance(result_list, list):
            raise TypeError("result_list should be of type list")
        if not isinstance(file_dict, dict):
            raise TypeError("file_dict should be of type dict")

        sorted_result_list = sorted(result_list)
        current_file = None
        current_line = 0

        for result in sorted_result_list:
            # print file name if appropriate
            if result.file != current_file:
                current_file = result.file
                current_line = 0
                print("\n{}".format(current_file))

            # print lines of file if appropriate
            if hasattr(result, "line_nr"):
                assert (current_file is not None), "A result with a line_nr should also have a file"
                assert (result.line_nr >= current_line), "Results with higher line_nr should be sorted further back"

                line_delta = result.line_nr - current_line
                if line_delta <= (padding_before + padding_after):  # line_padding larger than space available
                    for i in range(1, line_delta + 1):
                        print("|{real_nr:>4}{sign}{mod_nr:>4}|{symbol:1}{line}".format(real_nr=current_line + i,
                                                                                       sign="|",
                                                                                       mod_nr=current_line + i,
                                                                                       symbol="",
                                                                                       line=file_dict[result.file][
                                                                                           current_line + i - 1]))
                else:
                    for i in range(1, padding_after + 1):
                        print("|{real_nr:>4}{sign}{mod_nr:>4}|{symbol:1}{line}".format(real_nr=current_line + i,
                                                                                       sign="|",
                                                                                       mod_nr=current_line + i,
                                                                                       symbol="",
                                                                                       line=file_dict[result.file][
                                                                                           current_line + i - 1]))
                    for i in range(3):
                        print("|{real_nr:>4}{sign}{mod_nr:>4}|{symbol:1}{line}".format(real_nr="",
                                                                                       sign=".",
                                                                                       mod_nr="",
                                                                                       symbol="",
                                                                                       line=""))
                    for i in range(padding_before + 1):
                        print("|{real_nr:>4}{sign}{mod_nr:>4}|{symbol:1}{line}".format(real_nr=result.line_nr - i,
                                                                                       sign="|",
                                                                                       mod_nr=result.line_nr - i,
                                                                                       symbol="",
                                                                                       line=file_dict[result.file][
                                                                                           result.line_nr - i - 1]))
                    # at this point all needed lines including the current line should be shown
                    current_line = result.line_nr

                # now we just need to print the result
                message_string = "[{sev}] {bear}:\n{message}".format(sev=RESULT_SEVERITY.__str__(result.severity),
                                                                     bear=result.origin,
                                                                     message=result.message)
                message_string_list = message_string.split('\n')

                for i in range(message_string_list):
                    print("|{real_nr:>4}{sign}{mod_nr:>4}|{symbol:1}{line}".format(real_nr="",
                                                                                   sign="|",
                                                                                   mod_nr="",
                                                                                   symbol="",
                                                                                   line=message_string_list[i]))