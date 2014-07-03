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
from codeclib.internal.output.HTMLWriter import HTMLWriter
from codeclib.internal.output.Outputter import Outputter


class HTMLOutputter(Outputter):
    def __init__(self, filename, indentation_per_tag=2):
        Outputter.__init__(self)

        # backup old logfile, don't backup old backup
        if os.path.exists(filename):
            shutil.copy2(filename, filename+"~")

        self.writer = HTMLWriter(filename, indentation_per_tag)

    def print(self, *args, delimiter=' ', end=''):
        output = ""
        for arg in args:
            if output != "":
                output += delimiter
            output += arg

        self.writer.write_tags(p=output+end)

    def color_print(self, color, *args, delimiter=' ', end=''):
        output = ""
        for arg in args:
            if output != "":
                output += delimiter
            output += arg

        self.writer.write_tag("p", output+end, style="color:{}".format(color))
