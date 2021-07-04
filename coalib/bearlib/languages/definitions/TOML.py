from coalib.bearlib.languages.Language import Language


@Language
class TOML:
    extensions = '.toml',
    comment_delimiters = '#',
    string_delimiters = {'"': '"', "'": "'"}
    multiline_string_delimiters = {'"""': '"""', "'''": "'''"}
    encapsulators = {'[': ']', '{': '}'}
    special_chars = list(r'.,[]{}\=')
