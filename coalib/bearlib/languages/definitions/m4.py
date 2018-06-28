from coalib.bearlib.languages.Language import Language


@Language
class m4:
    extensions = '.m4',
    comment_delimiter = '#'
    encapsulators = {'(': ')', '{': '}'}
