from coalib.bearlib.languages.Language import Language


@Language
class Text:
    extensions = '.txt',
    multiline_comment_delimiters = {}
    comment_delimiters = ()
    string_delimiters = {}
    multiline_string_delimiters = {}
    indent_types = ()
    encapsulators = {}
    string_delimiter_escape = {}
