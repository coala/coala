import logging
from pygments.lexers import TextLexer
from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.style import Style
from pygments.token import Token


class NoColorStyle(Style):
    styles = {
        Token: 'noinherit'
    }


class BackgroundMessageStyle(Style):
    styles = {
        Token: 'bold bg:#eee #111'
    }


def fail_acquire_settings(log_printer, settings_names_dict):
    """
    This method throws an exception if any setting needs to be acquired.

    :param log_printer:         Printer responsible for logging the messages.
    :param settings_names_dict: A dictionary with the settings name as key and
                                a list containing a description in [0] and the
                                name of the bears who need this setting in [1]
                                and following.
    :raises AssertionError:     If any setting is required.
    :raises TypeError:          If ``settings_names_dict`` is not a
                                dictionary.
    """
    if not isinstance(settings_names_dict, dict):
        raise TypeError('The settings_names_dict parameter has to be a '
                        'dictionary.')

    required_settings = settings_names_dict.keys()
    if len(required_settings) != 0:
        msg = ('During execution, we found that some required '
               'settings were not provided. They are:\n')

        for name, setting in settings_names_dict.items():
            msg += '{} (from {}) - {}'.format(name, setting[1], setting[0])

        logging.error(msg)
        raise AssertionError(msg)


def highlight_text(no_color, text, style, lexer=TextLexer()):
    formatter = TerminalTrueColorFormatter(style=style)
    if no_color:
        formatter = TerminalTrueColorFormatter(style=NoColorStyle)
    return highlight(text, lexer, formatter)[:-1]


def color_letter(console_printer, line):
    x = -1
    y = -1
    letter = ''
    for i, l in enumerate(line, 0):
        if line[i] == '(':
            x = i
        if line[i] == ')':
            y = i
        if l.isupper() and x != -1:
            letter = l
    first_part = line[:x+1]
    second_part = line[y:]

    console_printer.print(first_part, end='')
    console_printer.print(letter, color='blue', end='')
    console_printer.print(second_part)


def format_lines(lines, symbol='', line_nr=''):
    def sym(x): return ']' if x is '[' else x
    return '\n'.join('{}{:>4}{} {}'.format(symbol, line_nr, sym(symbol), line)
                     for line in lines.rstrip('\n').split('\n'))
