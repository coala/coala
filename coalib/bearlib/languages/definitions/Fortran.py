from coalib.bearlib.languages.Language import Language


@Language
class Fortran:
    extensions = '.f90', '.f95', '.f03', '.f', '.for'
    comment_delimiter = '!'
