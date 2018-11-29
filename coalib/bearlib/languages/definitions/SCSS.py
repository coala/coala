from coalib.bearlib.languages.Language import Language


@Language
class SCSS:
    extensions = '.scss',
    comment_delimiters = '//',
    multiline_comment_delimiters = {'/*': '*/'}
    string_delimiters = {'"': '"', "'": "'"}
    multiline_string_delimiters = {}
    encapsulators = {'(': ')', '[': ']'}
    versions = {3.1, 3.2, 3.3, 3.4, 3.5, 4.0}
    interpolation = {'{': '}'}
