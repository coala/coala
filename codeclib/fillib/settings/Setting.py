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
from collections import OrderedDict


def path(obj):
    assert (type(obj) == Setting)
    obj.__path__()


class Setting: #TODO: maybe have to_string(), to_path() in addition to __bool__() etc? I'm at least not happy with having to import the path function to get a path.
    def __init__(self, key, value, origin):
        self.key = key
        self.value = value
        self.origin = origin

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        true_strings  = ['1', 'on',  'y', 'yes', 'yeah', 'always', 'sure', 'true', 'definitely', 'yup']
        false_strings = ['0', 'off', 'n', 'no',  'nope', 'never',  'nah',  'false']
        if self.value in true_strings:
            return True
        if self.value in false_strings:
            return False
        raise AttributeError

    def __int__(self):
        return int(self.value)

    def __len__(self):
        return len(self.value)

    def __path__(self):
        raise NotImplementedError
