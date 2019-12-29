from coalib.bearlib.languages.Language import Language


@Language
class Matlab:
    aliases = 'Octave',
    extensions = 'tuple'
    comment_delimiters = '%',
