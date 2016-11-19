import unittest

from coalib.misc.Exceptions import get_exitcode
from pkg_resources import VersionConflict


class ExceptionsTest(unittest.TestCase):

    def test_get_exitcode(self):
        self.assertEqual(get_exitcode(KeyboardInterrupt()), 130)
        self.assertEqual(get_exitcode(AssertionError()), 255)
        self.assertEqual(get_exitcode(SystemExit(999)), 999)
        self.assertEqual(get_exitcode(VersionConflict(
            'libclang-py3 0.3', 'libclang-py3==0.2')), 13)
        self.assertEqual(get_exitcode(EOFError()), 0)
        self.assertEqual(get_exitcode(None), 0)
