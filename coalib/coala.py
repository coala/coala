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

from pyprint.ConsolePrinter import ConsolePrinter

from coalib.misc.Constants import configure_logging
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.misc.Exceptions import get_exitcode


def main():
    configure_logging()

    try:
        console_printer = ConsolePrinter()
        log_printer = LogPrinter(console_printer)
        # Note: We parse the args here once to check whether to show bears or
        # not.
        args = default_arg_parser().parse_args()

        # Defer imports so if e.g. --help is called they won't be run
        from coalib.coala_modes import (
            mode_format, mode_json, mode_non_interactive, mode_normal)
        from coalib.output.ConsoleInteraction import (
            show_bears, show_language_bears_capabilities)

        console_printer = ConsolePrinter(print_colored=not args.no_color)

        if args.json:  # needs to be checked in order to display bears in json
            return mode_json(args)

        if args.show_bears:
            from coalib.settings.ConfigurationGathering import (
                get_filtered_bears)

            local_bears, global_bears = get_filtered_bears(
                args.filter_by_language, log_printer)

            show_bears(local_bears,
                       global_bears,
                       args.show_description or args.show_details,
                       args.show_details,
                       console_printer)

            return 0
        elif args.show_capabilities:
            from coalib.collecting.Collectors import (
                filter_capabilities_by_languages)
            from coalib.settings.ConfigurationGathering import (
                get_filtered_bears)

            local_bears, global_bears = get_filtered_bears(
                args.filter_by_language, log_printer)
            capabilities = filter_capabilities_by_languages(
                local_bears, args.show_capabilities)
            show_language_bears_capabilities(capabilities, console_printer)

            return 0

    except BaseException as exception:  # pylint: disable=broad-except
        return get_exitcode(exception, log_printer)

    if args.non_interactive:
        return mode_non_interactive(console_printer, args)

    if args.format:
        return mode_format()

    return mode_normal(console_printer, log_printer)


if __name__ == '__main__':  # pragma: no cover
    main()
