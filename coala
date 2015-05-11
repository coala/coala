#!/usr/bin/env python3

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

import sys
from coalib.output.ClosableObject import ClosableObject

from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.misc.StringConstants import StringConstants
from coalib.processes.SectionExecutor import SectionExecutor
from coalib.settings.SectionManager import SectionManager


from coalib.misc.i18n import _


if __name__ == "__main__":
    log_printer = None
    interactor = None
    exitcode = 0
    try:
        did_nothing = True
        yielded_results = False
        sections, local_bears, global_bears, targets, interactor, log_printer \
            = SectionManager().run()
        for section_name in sections:
            section = sections[section_name]
            if not section.is_enabled(targets):
                continue

            yielded_results = yielded_results or SectionExecutor(
                section=section,
                global_bear_list=global_bears[section_name],
                local_bear_list=local_bears[section_name],
                interactor=interactor,
                log_printer=log_printer).run()
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
    except SystemExit as e:
        exitcode = e.code
    except:
        exception = sys.exc_info()[1]
        UNKNOWN_ERROR = _("An unknown error occurred.") + " " + \
                        StringConstants.THIS_IS_A_BUG
        DESCRIPTION = _("During execution of coala an exception was raised. "
                        "This should never happen. When asked for, the "
                        "following information may help investigating:")

        if log_printer is None:
            log_printer = ConsolePrinter()

        log_printer.log_exception(UNKNOWN_ERROR + " " + DESCRIPTION,
                                  exception)
        exitcode = 255

    if log_printer is not None and isinstance(log_printer, ClosableObject):
        log_printer.close()
    if interactor is not None and isinstance(interactor, ClosableObject):
        interactor.close()

    exit(exitcode)
