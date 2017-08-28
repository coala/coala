from coalib.bearlib.languages.Language import Language


@Language
class Golang:
    aliases = 'go',
    extensions = '.go',
    comment_delimiter = '//'
    multiline_comment_delimiters = {'/*': '*/'}
    string_delimiters = {'"': '"'}
    multiline_string_delimiters = {'`': '`'}
    indent_types = {'{': '}'}
    encapsulators = {'(': ')', '[': ']'}
