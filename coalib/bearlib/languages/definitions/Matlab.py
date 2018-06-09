from coalib.bearlib.languages.Language import Language


@Language
class Matlab:
    aliases = 'Octave',
    extensions = '.m'
    comment_delimiter = '%'
