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
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


class Process:
    @staticmethod
    def __fileprocess(settings, file, localfilters):
        pass

    @staticmethod
    def __filterprocess(settings, files, globalfilter):
        pass

    @staticmethod
    def startProcesses(settings, filters):
        # TODO __fileprocess for each file (alphabetical)
        # hold outputs for an alphabetical order

        # start filterprocess'es after that, hold outputs till all
        # fileprocesses finished
        pass

    @staticmethod
    def waitForEnd(self):
        pass
