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

import logging
import sys

from pyprint.ConsolePrinter import ConsolePrinter

from dependency_management.requirements.PipRequirement import PipRequirement

from coalib.parsing.FilterHelper import (
    apply_filter, apply_filters, InvalidFilterException)
from coalib.output.Logging import configure_logging
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.misc.Exceptions import get_exitcode


def main(debug=False):
    configure_logging()

    args = None  # to have args variable in except block when parse_args fails
    try:
        # Note: We parse the args here once to check whether to show bears or
        # not.
        args = default_arg_parser().parse_args()
        if args.debug:
            req_ipdb = PipRequirement('ipdb')
            if not req_ipdb.is_installed():
                logging.error('--debug flag requires ipdb. '
                              'You can install it with:\n%s',
                              ' '.join(req_ipdb.install_command()))
                sys.exit(13)

        if debug or args.debug:
            args.log_level = 'DEBUG'

        # Defer imports so if e.g. --help is called they won't be run
        from coalib.coala_modes import (
            mode_format, mode_json, mode_non_interactive, mode_normal)
        from coalib.output.ConsoleInteraction import (
            show_bears, show_language_bears_capabilities)

        console_printer = ConsolePrinter(print_colored=not args.no_color)
        configure_logging(not args.no_color)

        if args.json and args.format:
            sys.exit(2)

        if args.show_bears:
            from coalib.settings.ConfigurationGathering import get_all_bears
            kwargs = {}
            if args.bears:
                kwargs['bear_globs'] = args.bears
            filtered_bears = get_all_bears(**kwargs)
            if args.filter_by_language:
                logging.warning(
                    "'--filter-by-language ...' is deprecated. "
                    "Use '--filter-by language ...' instead.")
                if args.filter_by is None:
                    args.filter_by = []
                args.filter_by.append(['language'] + args.filter_by_language)
            if args.filter_by:
                # Each iteration of the following loop applies
                # filters one by one provided as arguments
                try:
                    filtered_bears = apply_filters(
                        args.filter_by, filtered_bears)
                except InvalidFilterException as ex:
                    # If filter is not available
                    console_printer.print(ex)
                    return 2

            local_bears, global_bears = filtered_bears
            show_bears(local_bears,
                       global_bears,
                       args.show_description or args.show_details,
                       args.show_details,
                       console_printer,
                       args)

            return 0
        elif args.show_capabilities:
            from coalib.collecting.Collectors import (
                filter_capabilities_by_languages)
            local_bears, _ = apply_filter('language', args.show_capabilities)
            capabilities = filter_capabilities_by_languages(
                local_bears, args.show_capabilities)
            show_language_bears_capabilities(capabilities, console_printer)

            return 0

        if args.json:
            return mode_json(args, debug=debug)

    except BaseException as exception:  # pylint: disable=broad-except
        if not isinstance(exception, SystemExit):
            if args and args.debug:
                import ipdb
                with ipdb.launch_ipdb_on_exception():
                    raise

            if debug:
                raise

        return get_exitcode(exception)

    if args.format:
        return mode_format(args, debug=debug)

    if args.non_interactive:
        return mode_non_interactive(console_printer, args, debug=debug)

    return mode_normal(console_printer, None, args, debug=debug)


if __name__ == '__main__':  # pragma: no cover
    main()
