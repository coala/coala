from coalib.bearlib.languages.Language import Language


@Language
class Jinja2:
    extensions = '.jj2', '.j2', '.jinja', '.jinja2'
    multiline_comment_delimiters = {'{#': '#}'}
