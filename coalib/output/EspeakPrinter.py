"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import subprocess

from coalib.misc.StringConstants import StringConstants
from coalib.output.Printer import Printer
from coalib.misc.i18n import _


class EspeakPrinter(Printer):
    def __init__(self):
        """
        Raises EnvironmentError if VoiceOutput is impossible.
        """
        Printer.__init__(self)
        # TODO retrieve language from get_locale and select appropriate voice

        try:
            self.espeak = subprocess.Popen(['espeak'], stdin=subprocess.PIPE)
        except OSError:  # pragma: no cover
            print(_("Espeak doesn't seem to be installed. You cannot use the voice output feature without espeak. "
                    "It can be downloaded from http://espeak.sourceforge.net/ or installed via your usual package "
                    "repositories."))
            raise EnvironmentError
        except:  # pragma: no cover
            print(_("Failed to execute espeak. An unknown error occurred."), StringConstants.THIS_IS_A_BUG)
            raise EnvironmentError

    def __del__(self):
        self.espeak.stdin.close()

    def _print(self, output, **kwargs):
        self.espeak.stdin.write(output.encode())
        self.espeak.stdin.flush()
