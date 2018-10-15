from coalib.bearlib.languages.Language import Language


@Language
class SASS:
    extensions = '.sass',
    comment_delimiters = '//',
    multiline_comment_delimiters = {'/*': '*/'}
    encapsulators = {'(': ')', '[': ']'}
    interpolation = {'{': '}'}
    keywords = [
        'include', 'not', 'to', 'through', 'if', 'for', 'each',
        'while', 'mixin', 'import', 'media', 'extend', 'at-root',
        'debug', 'warn', 'error']
    special_chars = list('{}()&/@*,;>')
