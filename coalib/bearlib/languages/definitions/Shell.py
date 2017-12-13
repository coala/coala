from coalib.bearlib.languages.Language import Language


@Language
class Shell:
    aliases = 'bash', 'sh'

    extensions = '.sh', '.bash', '.zsh'
    comment_delimiter = '#'
    multiline_comment_delimiters = {": '": "'"}
    string_delimiters = {'"': '"', "'": "'", '`': '`'}
    multiline_string_delimiters = string_delimiters
    encapsulators = {'[': ']', '{': '}'}
    keywords = [
        'if', 'then', 'else', 'elif', 'fi', 'case', 'coproc', 'esac',
        'for', 'select', 'while', 'until', 'do', 'done', 'in',
        'function']
    special_chars = list('{}!|><[]')
