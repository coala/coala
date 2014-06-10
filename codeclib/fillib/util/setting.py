__author__ = 'lasse'


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
            for elem in self.value:
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
        if index is None:
            if self.value and self.value != [None]:
                bool_list = []
                for str in self.value:
                    if str in ['y', 'yes', 'yeah', 'always', 'sure', 'definitely', 'yup', 'true']:
                        bool_list.append(True)
                    elif str in ['n', 'no', 'nope', 'never', 'nah', 'false']:
                        bool_list.append(False)
                    elif str in ['', 'None', 'none']:
                        bool_list.append(None)
                    else:
                        bool_list.append(default)
                return bool_list
            else:  # value is None, [], or [None]
                return default
        else:  # index is set
            try:
                if self.value[index] in ['y', 'yes', 'yeah', 'always', 'sure', 'definitely', 'yup', 'true']:
                    return [True]
                elif self.value[index] in ['n', 'no', 'nope', 'never', 'nah', 'false']:
                    return [False]
                elif self.value[index] in ['', 'None', 'none']:
                    return [None]
            except AttributeError:
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


