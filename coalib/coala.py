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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import functools

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.coala_main import run_coala
from coalib.collecting.Collectors import (
    collect_all_bears_from_sections, filter_section_bears_by_languages)
from coalib.misc.Exceptions import get_exitcode
from coalib.output.ConsoleInteraction import (
    acquire_settings, nothing_done, print_results, print_section_beginning,
    show_bears)
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.settings.ConfigurationGathering import load_configuration


def main():
    try:
        console_printer = ConsolePrinter()
        log_printer = LogPrinter(console_printer)
        # Note: We parse the args here once to check whether to show bears or
        # not.
        args = default_arg_parser().parse_args()

        if args.show_bears:
            sections, _ = load_configuration(arg_list=None,
                                             log_printer=log_printer)
            local_bears, global_bears = collect_all_bears_from_sections(
                sections, log_printer)
            if args.filter_by_language:
                local_bears = filter_section_bears_by_languages(
                    local_bears, args.filter_by_language)
                global_bears = filter_section_bears_by_languages(
                    global_bears, args.filter_by_language)

            show_bears(local_bears,
                       global_bears,
                       args.show_description or args.show_details,
                       args.show_details,
                       console_printer)
            return 0
    except BaseException as exception:  # pylint: disable=broad-except
        return get_exitcode(exception, log_printer)

    partial_print_sec_beg = functools.partial(
        print_section_beginning,
        console_printer)
    results, exitcode, _ = run_coala(
        print_results=print_results,
        acquire_settings=acquire_settings,
        print_section_beginning=partial_print_sec_beg,
        nothing_done=nothing_done)

    return exitcode


if __name__ == '__main__':  # pragma: no cover
    main()
