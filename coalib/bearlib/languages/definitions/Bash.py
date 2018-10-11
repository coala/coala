from coalib.bearlib.languages.Language import Language


@Language
class Bash:
    extensions = '.bash',
    comment_delimiters = '#',
    multiline_comment_delimiters = {": '": "'"}
    string_delimiters = {'"': '"', "'": "'", '`': '`'}
    multiline_string_delimiters = string_delimiters
    encapsulators = {'[': ']', '{': '}'}
    keywords = [
        'if', 'then', 'else', 'elif', 'fi', 'case', 'esac',
        'for', 'select', 'while', 'until', 'do', 'done', 'in',
        'function', 'time',
        ]
    special_chars = list('{}!|><[]*?$')
