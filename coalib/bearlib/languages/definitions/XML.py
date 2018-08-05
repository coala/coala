from coalib.bearlib.languages.Language import Language


@Language
class XML:
    __qualname__ = 'Extensible Markup Language'
    aliases = 'xml',
    versions = 1.0,

    extensions = '.xml',
    multiline_comment_delimiters = {'<!--': '-->'}
    string_delimiters = {'"': '"', "'": "'", '<![CDATA[': ']]>'}
    multiline_string_delimiters = string_delimiters
    encapsulators = {'<': '>'}
