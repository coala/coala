from coalib.bearlib.languages.Language import Language


@Language
class Python:
    aliases = 'py',
    versions = 2.7, 3.3, 3.4, 3.5, 3.6

    extensions = '.py',
    comment_delimiter = '#'
    multiline_comment_delimiters = {}
    string_delimiters = {'"': '"', "'": "'"}
    multiline_string_delimiters = {'"""': '"""', "'''": "'''"}
    indent_types = ':',
    encapsulators = {'(': ')', '[': ']', '{': '}'}
