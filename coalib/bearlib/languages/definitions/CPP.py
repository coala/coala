from coalib.bearlib.languages.Language import Language


@Language
class CPP:
    aliases = 'C++', 'C Plus Plus', 'CPlusPlus', 'CXX'

    extensions = '.c', '.cpp', '.h', '.hpp'
    comment_delimiter = '//'
    multiline_comment_delimiters = {'/*': '*/'}
    string_delimiters = {'"': '"'}
    multiline_string_delimiters = {'R("': ')"'}
    indent_types = {'{': '}'}
    encapsulators = {'(': ')', '[': ']'}
    keywords = [
        'alignas', 'alignof', 'and', 'and_eq', 'asm', 'auto', 'bitand',
        'bitor', 'bool', 'break', 'case', 'catch', 'char', 'char16_t',
        'char32_t', 'class', 'compl', 'concept', 'const', 'constexpr',
        'const_cast', 'continue', 'decltype', 'default', 'delete', 'do',
        'double', 'dynamic_cast', 'else', 'enum', 'explicit', 'export',
        'extern', 'false', 'float', 'for', 'friend', 'goto', 'if', 'inline',
        'int', 'long', 'mutable', 'namespace', 'new', 'noexcept', 'not',
        'not_eq', 'nullptr', 'operator', 'or', 'or_eq', 'private',
        'protected', 'public', 'register', 'reinterpret_cast', 'requires',
        'return', 'short', 'signed', 'sizeof', 'static', 'static_assert',
        'static_cast', 'struct', 'switch', 'template', 'this', 'thread_local',
        'throw', 'true', 'try', 'typedef', 'typeid', 'typename', 'union',
        'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t',
        'while', 'xor', 'xor_eq', '#include', '#define', '#undef', '#ifdef',
        '#ifndef', '#if', '#endif', '#else', '#elif', '#line', '#pragma']
    special_chars = list('+-*/.;\,()[]{}\=<>|&^~?%!')
