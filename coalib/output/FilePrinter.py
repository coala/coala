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
from coalib.output.LOG_LEVEL import LOG_LEVEL
from coalib.output.LogPrinter import LogPrinter


class FilePrinter(LogPrinter):
    """
    This is a simple printer/logprinter that prints everything to a file. Note that everything will be appended.
    """
    def __init__(self, filename, log_level=LOG_LEVEL.WARNING, timestamp_format="%X"):
        """
        Creates a new FilePrinter. If the directory of the given file doesn't exist or if there's any access problems,
        an exception will be thrown.

        :param filename: the name of the file to put the data into (string).
        """
        self.file = None
        if not isinstance(filename, str):
            raise TypeError("filename must be a string.")

        LogPrinter.__init__(self, timestamp_format=timestamp_format, log_level=log_level)

        self.file = open(filename, 'a+')

    def __del__(self):
        if self.file is not None:
            self.file.close()

    def _print(self, output, **kwargs):
        self.file.write(output)
