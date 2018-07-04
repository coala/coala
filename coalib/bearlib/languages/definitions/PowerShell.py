from coalib.bearlib.languages.Language import Language


@Language
class PowerShell:
    extensions = '.ps1',
    comment_delimiters = '#',
    multiline_comment_delimiters = {'<#': '#>'}
    string_delimiters = {'"': '"', "'": "'"}
    multiline_string_delimiters = string_delimiters
    encapsulators = {'(': ')', '[': ']', '{': '}'}
