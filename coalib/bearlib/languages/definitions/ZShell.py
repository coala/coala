from coalib.bearlib.languages.Language import Language


@Language
class ZShell:
    extensions = '.zsh',
    comment_delimiters = '#',
    multiline_comment_delimiters = {": '": "'"}
    string_delimiters = {'"': '"', "'": "'", '`': '`'}
    multiline_string_delimiters = string_delimiters
    encapsulators = {'[': ']', '{': '}'}
    keywords = [
        'do', 'done', 'esac', 'then', 'elif', 'else',
        'fi', 'for', 'case', 'if', 'while', 'function',
        'repeat', 'time', 'until', 'select', 'coproc',
        'nocorrect', 'foreach', 'end', 'declare',
        'export', 'float', 'integer', 'local',
        'readonly', 'typeset',
        ]
    special_chars = list('{}!|><[]*?$')
