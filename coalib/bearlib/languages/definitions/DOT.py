from coalib.bearlib.languages.Language import Language


@Language
class DOT:
    aliases = 'DOT',
    extensions = '.gv', '.dot',
    comment_delimiters = '//', '#',
    multiline_comment_delimiters = {'/*': '*/'}
    string_delimiters = {'"': '"', '<': '>'}
    indent_types = {'{': '}'}
    encapsulators = {'(': ')', '[': ']'}
    keywords = [
        'node', 'edge', 'graph',
        'digraph', 'subgraph', 'strict',
        'shape', 'rank', 'parent',
        'label', 'labelloc', 'port',
    ]
    string_delimiter_escape = {"'": "\'"}
