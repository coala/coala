from coalib.bearlib.languages.Language import Language


@Language
class C:
    extensions = '.c', '.h'
    comment_delimiter = '//'
    multiline_comment_delimiters = {'/*': '*/'}
    string_delimiters = {'"': '"'}
    multiline_string_delimiters = {}
    indent_types = {'{': '}'}
    encapsulators = {'(': ')', '[': ']'}
    keywords = [
        'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
        'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
        'if', 'int', 'long', 'register', 'return', 'short', 'signed',
        'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
        'unsigned', 'void', 'volatile', 'while', '#include', '#define',
        '#undef', '#ifdef', '#ifndef', '#if', '#endif', '#else', '#elif',
        '#line', '#pragma']
    special_chars = list('+-*/.;\,()[]{}\=<>|&^~?%!')
