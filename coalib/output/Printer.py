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


class Printer:
    """
    A Printer is an object that can output (usually unformatted) text.

    This object is the base class of every printer and handles output concatenation to support the usual delimiter/end
    parameters. If you want to implement a Printer you want to override the _print method which takes just one string
    which is ready to be outputted.

    Examples for some printers are:
    - ConsolePrinter for console and file output
    - EspeakPrinter for Voice output
    - NullPrinter for no output
    """
    def _print(self, output, **kwargs):
        raise NotImplementedError

    def print(self, *args, delimiter=' ', end='\n', **kwargs):
        """
        Prints the given arguments to an output medium.

        :param args: Will be outputted.
        :param delimiter: Delimits the args.
        :param end: Will be appended in the end (without an additional delimiter)
        :param kwargs: Will be passed through to the Printer derivative handling the actual printing
        """
        output = str(delimiter).join(str(arg) for arg in args) + str(end)

        return self._print(output, **kwargs)
