from coalib.bearlib.languages.Language import Language


@Language
class HTML:
    __qualname__ = 'Hypertext Markup Language'
    versions = 2.0, 3.2, 4.0, 4.01, 5, 5.1

    extensions = '.html', '.htm'
    multiline_comment_delimiters = {'<!--': '-->'}
    string_delimiters = {'"': '"', "'": "'"}
    multiline_string_delimiters = string_delimiters
    encapsulators = {'<': '>'}
    encapsulators.update(string_delimiters)
