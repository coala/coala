from coalib.bearlib.languages.Language import Language


@Language
class Ruby:
    aliases = 'rb',
    extensions = '.rb',
    comment_delimiter = '#'
    multiline_comment_delimiters = {'=begin': '=end'}
    string_delimiters = {'"': '"', "'": "'", '%q(': ')', '%Q(': ')', '%(': ')'}
    encapsulators = {'[': ']', '{': '}', '%w(': ')', '%W(': ')'}
