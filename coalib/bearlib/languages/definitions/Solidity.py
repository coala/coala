from coalib.bearlib.languages.Language import Language


@Language
class Solidity:
    extensions = '.sol'
    comment_delimiters = '//',
    string_delimiters = {'"': '"'}
    multiline_string_delimiters = {}
    indent_types = {'{': '}'}
    keywords = [
        'address', 'bool', 'break', 'byte',
        'const', 'continue', 'do', 'else',
        'emit', 'enum', 'false', 'float',
        'for', 'function', 'goto', 'if',
        'int', 'long', 'pragma', 'return',
        'string', 'struct', 'throw', 'true',
        'uint', 'while']
