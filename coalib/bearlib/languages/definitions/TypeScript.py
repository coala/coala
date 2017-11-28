from coalib.bearlib.languages.Language import Language


@Language
class TypeScript:
    aliases = 'ts'
    extensions = '.ts', '.tsx'
    comment_delimiter = '//'
    multiline_comment_delimiters = {'/*': '*/'}
    string_delimiters = {'"': '"', "'": "'"}
    multiline_string_delimiters = {'`': '`'}
    indent_types = {'{': '}'}
    encapsulators = {'(': ')', '[': ']'}
    keywords = [
                    'break', 'case', 'catch', 'class', 'const',
                    'async', 'await',
                    'continue', 'debugger', 'default', 'delete',
                    'do', 'else', 'enum', 'export', 'extends',
                    'false', 'finally', 'for', 'function', 'if', 'import',
                    'in', 'instanceof', 'new', 'null', 'return', 'super',
                    'switch', 'this', 'throw', 'true', 'try', 'typeof',
                    'var', 'void', 'while', 'with', 'as', 'implements',
                    'interface', 'let', 'package', 'private', 'protected',
                    'public', 'static', 'yield', 'any', 'boolean',
                    'constructor', 'declare', 'get',
                    'module', 'require', 'number', 'set',
                    'string', 'symbol', 'type', 'from', 'of']
