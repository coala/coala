# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from coalib.output.ConsoleInteraction import (nothing_done,
                                              acquire_settings,
                                              print_section_beginning,
                                              print_results,
                                              finalize,
                                              show_bears)
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.processes.Processing import execute_section
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.misc.Exceptions import get_exitcode


def main():
    log_printer = LogPrinter(ConsolePrinter())
    console_printer = ConsolePrinter()
    exitcode = 0
    try:
        did_nothing = True
        yielded_results = False
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(acquire_settings, log_printer)

        if bool(sections["default"].get("show_bears", "False")):
            show_bears(local_bears,
                       global_bears,
                       console_printer)
            did_nothing = False
        else:
            for section_name in sections:
                section = sections[section_name]
                if not section.is_enabled(targets):
                    continue

                file_diff_dict = {}
                print_section_beginning(console_printer, section)
                results = execute_section(
                    section=section,
                    global_bear_list=global_bears[section_name],
                    local_bear_list=local_bears[section_name],
                    print_results=print_results,
                    log_printer=log_printer,
                    file_diff_dict=file_diff_dict)
                yielded_results = yielded_results or results[0]
                finalize(file_diff_dict, results[3], log_printer)
                did_nothing = False

        if did_nothing:
            nothing_done(console_printer)

        if yielded_results:
            exitcode = 1
    except BaseException as exception:  # pylint: disable=broad-except
        exitcode = exitcode or get_exitcode(exception, log_printer)

    return exitcode
