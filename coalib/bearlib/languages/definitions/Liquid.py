from coalib.bearlib.languages.Language import Language


@Language
class Liquid:
    extensions = '.liquid',
    multiline_comment_delimiters = {'{% comment %}': '{% endcomment %}'}
    string_delimiters = {'"': '"', "'": "'"}
