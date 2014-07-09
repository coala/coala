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
import shutil
from coalib.internal.output.Outputter import Outputter


class LogFileOutputter(Outputter):
    def __init__(self, filename):
        Outputter.__init__(self)

        # backup old logfile, don't backup old backup
        if os.path.exists(filename):
            shutil.copy2(filename, filename+"~")

        self.file = open(filename, "w")

    def __del__(self):
        self.file.close()

    def print(self, *args, delimiter=' ', end='\n', color=None, log_date=True):
        # TODO place log date in front of message, search for \n's in message
        output = ""
        for arg in args:
            if output != "":
                output += delimiter
            output += arg

        self.file.write(output + end)
