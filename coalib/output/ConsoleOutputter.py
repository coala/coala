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
    def __init__(self, output=sys.stdout, log_level=LOG_LEVEL.WARNING, timestamp_format="%X"):
        Outputter.__init__(self)
        ConsolePrinter.__init__(self, output=output, log_level=log_level, timestamp_format=timestamp_format)

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
