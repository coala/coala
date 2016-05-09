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
from coalib.settings.SectionFilling import fill_settings


def main():
    # Note: We parse the args here once to check whether to show bears or not.
    arg_parser = default_arg_parser()
    args = arg_parser.parse_args()

    console_printer = ConsolePrinter()
    if args.show_bears or args.show_all_bears or args.show_language_bears:
        log_printer = LogPrinter(console_printer)
        try:
            sections, _ = load_configuration(arg_list=None,
                                             log_printer=log_printer)
            if args.show_language_bears:
                local_bears, global_bears = collect_all_bears_from_sections(
                    sections, log_printer)
                local_bears = filter_section_bears_by_languages(
                    local_bears, args.show_language_bears)
                global_bears = filter_section_bears_by_languages(
                    global_bears, args.show_language_bears)
            elif args.show_all_bears:
                local_bears, global_bears = collect_all_bears_from_sections(
                    sections, log_printer)
            else:
                # We ignore missing settings as it's not important.
                local_bears, global_bears = fill_settings(
                    sections,
                    acquire_settings=lambda *args, **kwargs: {},
                    log_printer=log_printer)
            show_bears(local_bears, global_bears,
                       args.show_language_bears or args.show_all_bears,
                       console_printer)
        except BaseException as exception:  # pylint: disable=broad-except
            return get_exitcode(exception, log_printer)
        return 0

    partial_print_sec_beg = functools.partial(
        print_section_beginning,
        console_printer)
    results, exitcode, _ = run_coala(
        print_results=print_results,
        acquire_settings=acquire_settings,
        print_section_beginning=partial_print_sec_beg,
        nothing_done=nothing_done)

    return exitcode
