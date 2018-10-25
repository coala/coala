from coalib.bearlib.languages.Language import Language


@Language
class TinyBasic:
    aliases = 'tb',
    extensions = '.tb',
    comment_delimiters = 'REM', "'"
    string_delimiters = {'"': '"', "'": "'"}
    encapsulators = {'(': ')'}
    versions = {1.0, 2.0}
    keywords = [
        'PRINT', 'IF', 'THEN',
        'GOTO', 'INPUT', 'LET',
        'GOSUB', 'RETURN', 'CLEAR',
        'LIST', 'RUN', 'END',
        'PR', 'RND', 'USR',
    ]
    special_chars = list('+-*/<>=,;()[]')
