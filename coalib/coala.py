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
from coalib.misc.Exceptions import get_exitcode
from coalib.collecting.Collectors import filter_capabilities_by_languages
from coalib.output.ConsoleInteraction import (
    acquire_settings, nothing_done, print_results, print_section_beginning,
    show_bears, show_language_bears_capabilities)
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.settings.ConfigurationGathering import get_filtered_bears


def main():
    try:
        console_printer = ConsolePrinter()
        log_printer = LogPrinter(console_printer)
        # Note: We parse the args here once to check whether to show bears or
        # not.
        args = default_arg_parser().parse_args()

        if args.show_bears:
            local_bears, global_bears = get_filtered_bears(
                args.filter_by_language, log_printer)

            show_bears(local_bears,
                       global_bears,
                       args.show_description or args.show_details,
                       args.show_details,
                       console_printer)

            return 0
        elif args.show_capabilities:
            local_bears, global_bears = get_filtered_bears(
                args.filter_by_language, log_printer)
            capabilities = filter_capabilities_by_languages(
                local_bears, args.show_capabilities)
            show_language_bears_capabilities(capabilities, console_printer)

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
