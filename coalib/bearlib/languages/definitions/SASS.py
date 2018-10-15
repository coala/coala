from coalib.bearlib.languages.Language import Language


@Language
class SASS:
    extensions = '.sass',
    comment_delimiters = '//',
    multiline_comment_delimiters = {'/*': '*/'}
    encapsulators = {'(': ')', '[': ']'}
    versions = {3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.0}
    interpolation = {'{': '}'}
    keywords = [
        'include', 'not', 'to', 'through', 'if', 'for', 'each',
        'while', 'mixin', 'import', 'media', 'extend', 'at-root',
        'debug', 'warn', 'error']
    special_chars = list('{}()&/@*,;>')
