from coalib.bearlib.languages.Language import Language


@Language
class VisualBasic:
    aliases = 'vb',
    extensions = '.vb', '.bas'
    comment_delimiter = "'", 'REM'
    string_delimiters = {'"': '"'}
    # Multiline strings are only supported by Visual Basic 14.0 and above
    multiline_string_delimiters = string_delimiters
    encapsulators = {'(': ')', '{': '}'}
    max_line_length = 65535
    string_delimiter_escape = {'"': '""'}
