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


class Setting:
    def __init__(self, key, value, import_history=None, comments_before=None, trailing_comment='', overrides=None):
        if import_history is None:
            import_history = []
        if comments_before is None:
            comments_before = []

        self.key = key
        self.value = value
        self.import_history = import_history
        self.comments_before = comments_before
        self.trailing_comment = trailing_comment
        self.overrides = overrides

    def generate_lines(self):
        result = []
        for comment in self.comments_before:
            if comment is not None:
                if comment:
                    result.append('# '+comment)
                else:
                    result.append('')

        if self.key == '':
            return result

        line = self.key + ' = '
        if self.value is None:
            line += "None"
        else:
            delimiter = ''
            for elem     in self.value:
                line += delimiter + str(elem)
                delimiter = ", "

        if self.trailing_comment:
            line += ' # ' + self.trailing_comment
        result.append(line)
        return result

    def to_int(self, index = None, default = 0):
        if index is None:
            if self.value and self.value != [None]and self.value != ['None']:
                int_list = []
                for str in self.value:
                    try:
                        int_list.append(int(str))
                    except ValueError:
                        int_list.append(default)
                return int_list
            else:  # value is None, [], or [None]
                return []
        else:  # index is set
            try:
                return int(self.value[index])
            except:
                return default


    def to_bool(self, index = None, default = None):
        true_strings = ['1', 'y', 'yes', 'yeah', 'always', 'sure', 'definitely', 'yup', 'true']
        false_strings = ['0', 'n', 'no', 'nope', 'never', 'nah', 'false']
        none_strings = ['', 'None', 'none']
        if index is None:
            if self.value and self.value != [None]:
                bool_list = []
                for str in self.value:
                    if str in true_strings:
                        bool_list.append(True)
                    elif str in false_strings:
                        bool_list.append(False)
                    elif str in none_strings:
                        bool_list.append(None)
                    else:
                        bool_list.append(default)
                return bool_list
            else:  # value is None, [], or [None]
                return default
        else:  # index is set
            try:
                if self.value[index].lower() in true_strings:
                    return True
                elif self.value[index].lower() in false_strings:
                    return False
                elif self.value[index].lower() in none_strings:
                    return None
            except AttributeError:
                print("Exception in to_bool with set index for setting:", self.key)
                return default

    def to_color_code(self, index = None):

        color_code_dict = {
            'black': '\033[0;30m',
            'bright gray': '\033[0;37m',
            'blue': '\033[0;34m',
            'white': '\033[1;37m',
            'green': '\033[0;32m',
            'bright blue': '\033[1;34m',
            'cyan': '\033[0;36m',
            'bright green': '\033[1;32m',
            'red': '\033[0;31m',
            'bright cyan': '\033[1;36m',
            'purple': '\033[0;35m',
            'bright red': '\033[1;31m',
            'yellow': '\033[0;33m',
            'bright purple': '\033[1;35m',
            'dark gray': '\033[1;30m',
            'bright yellow': '\033[1;33m',
            'normal': '\033[0m'}

        if index is None:
            if self.value and self.value != [None]and self.value != ['None']:
                color_list = []
                for str in self.value:
                    try:
                        color_list.append(color_code_dict[str.lower()])
                    except:
                        color_list.append(color_code_dict["normal"])
                return color_list
            else:  # value is None, [], or [None]
                return []
        else:  # index is set
            try:
                return color_code_dict[self.value[index].lower()]
            except:
                return color_code_dict["normal"]
        pass


