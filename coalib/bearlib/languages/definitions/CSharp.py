from coalib.bearlib.languages.Language import Language


@Language
class CSharp:
    __qualname__ = 'C#'
    aliases = 'CS',
    extensions = '.cs',
    comment_delimiters = '//',
    multiline_comment_delimiters = {'/*': '*/'}
    string_delimiters = {'"': '"'}
    string_delimiter_escape = {'"': '\\"'}
