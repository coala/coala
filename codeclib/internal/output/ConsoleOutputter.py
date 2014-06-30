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
from codeclib.internal.output.Outputter import Outputter


class ConsoleOutputter(Outputter):
    def __init__(self):
        Outputter.__init__(self)

    def print(self, *args, delimiter=' ', end='\n'):
        for arg in args:
            print(arg, end=delimiter)
        print(end=end)

    def color_print(self, color, *args, delimiter=' ', end='\n'):
        color_code_dict = {
            'black': '0;30', 'bright gray': '0;37',
            'blue': '0;34', 'white': '1;37',
            'green': '0;32', 'bright blue': '1;34',
            'cyan': '0;36', 'bright green': '1;32',
            'red': '0;31', 'bright cyan': '1;36',
            'purple': '0;35', 'bright red': '1;31',
            'yellow': '0;33', 'bright purple': '1;35',
            'dark gray': '1;30', 'bright yellow': '1;33',
            'normal': '0',
        }
        try:
            print('\033[' + color_code_dict.get(color, '0') + 'm', end='')
            for arg in args:
                print(arg, end=delimiter)
            print('\033[0m', end=end)
        except:
            self.print(args, delimiter=delimiter, end=end)