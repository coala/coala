from coalib.bearlib.languages.Language import Language


@Language
class D:
    extensions = '.d',
    comment_delimiters = '//',
    string_delimiters = {'"': '"'}
    multiline_comment_delimiters = {'/*': '*/'}
    indent_types = {'{': '}'}
    encapsulators = {'(': ')', '[': ']'}
    keywords = [
        'abstract', 'alias', 'align', 'asm', 'assert', 'auto', 'body', 'bool',
        'break', 'byte', 'case', 'cast', 'catch', 'cdouble', 'cent', 'cfloat',
        'char', 'class', 'const', 'continue', 'creal', 'dchar', 'debug',
        'default', 'delegate', 'delete', 'deprecated', 'do', 'double', 'else',
        'enum', 'export', 'extern', 'false', 'final', 'finally', 'float',
        'for', 'foreach', 'foreach_reverse', 'function', 'goto', 'idouble',
        'if', 'ifloat', 'immutable', 'import', 'in', 'inout', 'int',
        'interface', 'invariant', 'ireal', 'is', 'lazy', 'long', 'macro',
        'mixin', 'module', 'new', 'nothrow', 'null', 'out', 'override',
        'package', 'pragma', 'private', 'protected', 'public', 'pure', 'real',
        'ref', 'return', 'scope', 'shared', 'short', 'static', 'struct',
        'super', 'switch', 'synchronized', 'template', 'this', 'throw', 'true',
        'try', 'typedef', 'typeid', 'typeof', 'ubyte', 'ucent', 'uint',
        'ulong', 'union', 'unittest', 'ushort', 'version', 'void', 'wchar',
        'while', 'with', '__FILE__', '__FILE_FULL_PATH__', '__MODULE__',
        '__LINE__', '__FUNCTION__', '__PRETTY_FUNCTION__', '__gshared',
        '__traits', '__vector', '__parameters',
    ]
    special_chars = list(r'>+~/|}.^),{#=&!?@<$](%*[-')
    string_delimiter_escape = {'"': '\\"'}
