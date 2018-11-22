from coalib.bearlib.languages.Language import Language


@Language
class Dart:
    extensions = '.dart',
    comment_delimiters = '//',
    multiline_comment_delimiters = {'/*': '*/'}
    string_delimiters = {'"': '"', "'": "'"}
    multiline_string_delimiters = {'"""': '"""', "'''": "'''"}
    encapsulators = {'(': ')', '[': ']', '{': '}'}
    keywords = [
        'Function', 'abstract', 'as', 'assert', 'async', 'await', 'break',
        'case', 'catch', 'class', 'const', 'continue', 'covariant', 'default',
        'deferred', 'do', 'dynamic', 'else', 'enum', 'export', 'extends',
        'external', 'factory', 'false', 'final', 'finally', 'for', 'get',
        'hide', 'if', 'implements', 'import', 'in', 'interface', 'is',
        'library', 'mixin', 'new', 'null', 'on', 'operator', 'part', 'rethrow',
        'return', 'set', 'show', 'static', 'super', 'switch', 'sync', 'this',
        'throw', 'true', 'try', 'typedef', 'var', 'void', 'while', 'with',
        'yield',
        ]
