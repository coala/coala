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

from coalib.output.ConsoleInteractor import ConsoleInteractor
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.misc.StringConstants import StringConstants
from coalib.processes.Processing import execute_section
from coalib.settings.ConfigurationGathering import gather_configuration
from coalib.output.ShowBears import show_bears
from coalib.misc.i18n import _


def main():
    log_printer = ConsolePrinter()
    interactor = ConsoleInteractor(log_printer)
    exitcode = 0
    try:
        did_nothing = True
        yielded_results = False
        (sections,
         local_bears,
         global_bears,
         targets) = gather_configuration(interactor.acquire_settings,
                                         log_printer)

        if bool(sections["default"].get("show_bears", "False")):
            show_bears(local_bears,
                       global_bears,
                       interactor.show_bears)
            did_nothing = False
        else:
            for section_name in sections:
                section = sections[section_name]
                if not section.is_enabled(targets):
                    continue

                interactor.begin_section(section)
                results = execute_section(
                    section=section,
                    global_bear_list=global_bears[section_name],
                    local_bear_list=local_bears[section_name],
                    print_results=interactor.print_results,
                    log_printer=log_printer)
                yielded_results = yielded_results or results[0]
                interactor.finalize(results[3])
                did_nothing = False

        if did_nothing:
            interactor.did_nothing()

        if yielded_results:
            exitcode = 1
    except KeyboardInterrupt:  # Ctrl+C
        print(_("Program terminated by user."))
        exitcode = 130
    except EOFError:  # Ctrl+D
        print(_("Found EOF. Exiting gracefully."))
    except SystemExit as exception:
        exitcode = exception.code
    except Exception as exception:
        UNKNOWN_ERROR = _("An unknown error occurred.") + " " + \
                        StringConstants.THIS_IS_A_BUG
        DESCRIPTION = _("During execution of coala an exception was raised. "
                        "This should never happen. When asked for, the "
                        "following information may help investigating:")

        log_printer.log_exception(UNKNOWN_ERROR + " " + DESCRIPTION,
                                  exception)
        exitcode = 255

    return exitcode
