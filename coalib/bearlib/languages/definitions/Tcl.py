from coalib.bearlib.languages.Language import Language


@Language
class Tcl:
    aliases = 'Tcl/Tk',
    extensions = '.tcl',
    string_delimiters = {'"': '"'}
    multiline_string_delimiters = {'"': '"'}
    encapsulators = {'(': ')', '[': ']', '{': '}'}
