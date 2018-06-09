from coalib.bearlib.languages.Language import Language


@Language
class Markdown:
    extensions = [
        '.markdown', '.mdown', '.mkdn',
        '.md', '.mkd', '.mdwn', '.mdtxt',
        '.mdtext']
    multiline_comment_delimiters = {'<!--': '-->'}
