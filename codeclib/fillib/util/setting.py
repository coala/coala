__author__ = 'lasse'


class Setting:
    @staticmethod
    def capitalize_key(name):
        # TODO recognize default options
        return name

    def __init__(self, key, value, import_history='', comments_before='', trailing_comment='', overwrites=None):
        self.key = Setting.capitalize_key(key)
        self.value = value
        self.import_history = import_history
        self.comments_before = comments_before
        self.trailing_comment = trailing_comment
        self.overwrites = overwrites

    def generate_lines(self):
        result = []
        for comment in self.comments_before:
            result.append('# '+comment)

        if self.key == '':
            return result

        line = self.key + ' = '
        if self.value is None:
            line += "None"
        else:
            delimiter = ''
            for elem in self.value:
                line.append(delimiter + elem)
                delimiter = ", "

        line.append(' # ' + self.trailing_comment)
        result.append(line)
        return result
