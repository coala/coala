import unittest

from pyprint.NullPrinter import NullPrinter
from pyprint.ConsolePrinter import ConsolePrinter
from termcolor import colored

from coala_utils.ContextManagers import retrieve_stdout
from coalib.output.Interactions import (fail_acquire_settings,
                                        format_lines,
                                        color_letter,
                                        highlight_text)
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.ConsoleInteraction import (
        NoColorStyle, BackgroundMessageStyle)


class InteractionsTest(unittest.TestCase):

    def test_(self):
        log_printer = LogPrinter(NullPrinter())
        self.assertRaises(TypeError, fail_acquire_settings, log_printer, None)
        self.assertRaises(AssertionError,
                          fail_acquire_settings,
                          log_printer,
                          {'setting': ['description', 'bear']})
        self.assertEqual(fail_acquire_settings(log_printer, {}), None)

    def test_format_lines(self):
        prompt_msg = 'Enter a number: '
        prompt_msg_formatted = '[    ] Enter a number: '
        self.assertEqual(format_lines(
            prompt_msg, symbol='['), prompt_msg_formatted)

    def test_color_letter(self):
        with retrieve_stdout() as stdout:
            console_printer = ConsolePrinter(print_colored=True)
            first_part = 'Do ('
            letter = 'T'
            second_part = ')his'
            message = first_part + letter + second_part

            color_letter(console_printer, message)

            self.assertEqual(stdout.getvalue().strip(), first_part +
                             colored(letter, color='blue') + second_part)

    def test_highlight_text(self):
        msg = 'Some text present here.'
        self.assertEqual(highlight_text(no_color=True,
                                        text=msg,
                                        style=BackgroundMessageStyle), msg)
        self.assertEqual(highlight_text(no_color=False,
                                        text=msg,
                                        style=NoColorStyle), msg)
