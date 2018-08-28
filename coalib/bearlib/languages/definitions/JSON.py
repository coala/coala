from coalib.bearlib.languages.Language import Language


@Language
class JSON:
    __qualname__ = 'JavaScript Object Notation'
    aliases = 'json',

    extensions = '.json',
    string_delimiters = {'"': '"'}
    encapsulators = {'[': ']', '{': '}'}
