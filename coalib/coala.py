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

from coalib.output.ConsoleInteraction import (nothing_done,
                                              acquire_settings,
                                              print_section_beginning,
                                              print_results,
                                              show_bears)
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.coala_main import run_coala


def main():
    console_printer = ConsolePrinter()
    partial_show_bears = functools.partial(
        show_bears,
        console_printer=console_printer)
    partial_print_sec_beg = functools.partial(
        print_section_beginning,
        console_printer)
    results, exitcode = run_coala(
        show_bears=partial_show_bears,
        print_results=print_results,
        acquire_settings=acquire_settings,
        print_section_beginning=partial_print_sec_beg,
        nothing_done=nothing_done)

    return exitcode
