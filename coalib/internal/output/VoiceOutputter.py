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
import os
import subprocess
from coalib.internal.misc.StringConstants import StringConstants
from coalib.internal.output.Outputter import Outputter
from coalib.fillib.misc.i18n import get_locale, _


class VoiceOutputter(Outputter):
    def __init__(self):
        Outputter.__init__(self)
        # TODO retrieve language from get_locale and select appropriate voice

    def print(self, *args, delimiter=' ', end='\n'):
        output = ""
        for arg in args:
            if output != "":
                output += delimiter
            output += arg

        try:
            if subprocess.call(["espeak", output]) != 0:
                print(_("Failed to invoke espeak. Output was: {}").format(output))
        except FileNotFoundError:
            print(_("Espeak is not installed. You cannot use the voice output feature without espeak. "
                    "It can be downloaded from http://espeak.sourceforge.net/ or installed via your usual package "
                    "repositories."))
        except:
            print(_("Failed to execute espeak. An unknown error occurred."), StringConstants.ThisIsABug)

    def color_print(self, color, *args, delimiter=' ', end='\n'):
        self.print(args, delimiter=delimiter, end=end)
