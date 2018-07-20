import argparse
import re
import unittest
from unittest.mock import patch, Mock

# Imported and unused here, to ensure an ImportError occurs here
# instead of inside coalib.  Please install it for the test to pass.
import argcomplete

import coalib.parsing.DefaultArgParser

from coalib.collecting.Collectors import get_all_bears_names
from coalib.parsing.DefaultArgParser import (
    CustomFormatter,
    default_arg_parser,
)


def _get_arg(parser, arg):
    actions = parser.__dict__['_action_groups'][0].__dict__['_actions']
    args = [item for item in actions
            if arg in item.option_strings]
    return args[0]


class CustomFormatterTest(unittest.TestCase):

    def setUp(self):
        arg_parser = argparse.ArgumentParser(formatter_class=CustomFormatter)
        arg_parser.add_argument('-a',
                                '--all',
                                nargs='?',
                                const=True,
                                metavar='BOOL')
        arg_parser.add_argument('TARGETS',
                                nargs='*')
        self.output = arg_parser.format_help()

    def test_metavar_in_usage(self):
        match = re.search(r'usage:.+(-a \[BOOL\]).+\n\n',
                          self.output,
                          flags=re.DOTALL)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '-a [BOOL]')

    def test_metavar_not_in_optional_args_sections(self):
        match = re.search('optional arguments:.+(-a, --all).*',
                          self.output,
                          flags=re.DOTALL)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), '-a, --all')


class AutocompleteTest(unittest.TestCase):

    def setUp(self):
        self._old_argcomplete = coalib.parsing.DefaultArgParser.argcomplete

    def tearDown(self):
        coalib.parsing.DefaultArgParser.argcomplete = self._old_argcomplete

    def test_argcomplete_missing(self):
        if coalib.parsing.DefaultArgParser.argcomplete is not None:
            coalib.parsing.DefaultArgParser.argcomplete = None
        real_importer = __import__

        def import_if_not_argcomplete(arg, *args, **kw):
            if arg == 'argcomplete':
                raise ImportError('import missing: %s' % arg)
            else:
                return real_importer(arg, *args, **kw)

        mock = Mock(side_effect=import_if_not_argcomplete)
        with patch('builtins.__import__', new=mock):
            default_arg_parser()
        self.assertFalse(coalib.parsing.DefaultArgParser.argcomplete)

    def test_argcomplete_imported(self):
        if coalib.parsing.DefaultArgParser.argcomplete is not None:
            coalib.parsing.DefaultArgParser.argcomplete = None
        parser = default_arg_parser()
        self.assertEqual(coalib.parsing.DefaultArgParser.argcomplete,
                         argcomplete)
        arg = _get_arg(parser, '--bears')
        self.assertTrue(hasattr(arg, 'completer'))
        bears = list(arg.completer())
        self.assertEqual(bears, get_all_bears_names())

    def test_argcomplete_missing_other(self):
        if coalib.parsing.DefaultArgParser.argcomplete is not None:
            coalib.parsing.DefaultArgParser.argcomplete = None
        real_importer = __import__

        def import_if_not_bear_names(arg, *args, **kw):
            if arg == 'coalib.collecting.Collectors':
                raise ImportError('import missing: %s' % arg)
            else:
                return real_importer(arg, *args, **kw)

        mock = Mock(side_effect=import_if_not_bear_names)
        with patch('builtins.__import__', new=mock):
            parser = default_arg_parser()
        self.assertTrue(coalib.parsing.DefaultArgParser.argcomplete)
        arg = _get_arg(parser, '--bears')
        self.assertFalse(hasattr(arg, 'completer'))
