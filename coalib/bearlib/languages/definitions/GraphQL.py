from coalib.bearlib.languages.Language import Language


@Language
class GraphQL:
    aliases = 'graphql',
    extensions = '.graphql',
    comment_delimiters = '#',
    string_delimiters = {'"': '"'},
    encapsulators = {'[': ']', '(': ')'},
    indent_types = {'{': '}'},
    keywords = [
        'type', 'enum', 'return', 'query', 'mutation', 'subscription',
        'on', 'schema', 'null', 'interface', 'scalar', 'union', 'input',
        'fragment']
