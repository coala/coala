from coalib.bearlib.languages.Language import Language


@Language
class Haskell:
    extensions = '.hs',
    versions = 1.0, 1.1, 1.2, 1.3, 1.4, 98, 2010
    special_chars = list('!#$%&;*:+.,/<=>?@\\^_|-~')
    comment_delimiters = '--',
    multiline_comment_delimiters = {'{-': '-}'}
    keywords = [
        'case', 'of', 'infixl', 'foreign',
        'data', 'data family', 'default', 'type family',
        'deriving', 'instance', 'do', 'forall',
        'hiding', 'if', 'then', 'else', 'import',
        'infixr', 'let', 'in', 'mdo', 'module',
        'proc', 'qualified', 'rec', 'type', 'infix',
        'where', 'newtype', 'show']
