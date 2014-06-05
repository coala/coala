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
