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

from coalib.output.NullInteractor import NullInteractor
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.misc.StringConstants import StringConstants
from coalib.processes.Processing import execute_enabled_sections
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.misc.i18n import _


def main():
    log_printer = ConsolePrinter()
    interactor = NullInteractor(log_printer)
    exitcode = 0
    try:
        yielded_results = False
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(interactor.acquire_settings,
                                         log_printer)

        section_results = execute_enabled_sections(sections,
                                                   targets,
                                                   global_bears,
                                                   local_bears,
                                                   interactor,
                                                   log_printer)
        for results in section_results:
            yielded_results = yielded_results or results[0]

        if yielded_results:
            exitcode = 1
    except KeyboardInterrupt:  # Ctrl+C
        log_printer.warn(_("Program terminated by user."))
        exitcode = 130
    except EOFError:  # Ctrl+D
        log_printer.debug(_("Found EOF. Exiting gracefully."))
    except SystemExit as exception:
        exitcode = exception.code
    except Exception as exception:  # pylint: disable=broad-except
        log_printer.log_exception(StringConstants.CRASH_MESSAGE, exception)
        exitcode = 255

    return exitcode
