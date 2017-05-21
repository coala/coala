import unittest

from coalib.output.Interactions import fail_acquire_settings
from coalib.settings.Section import Section


class InteractionsTest(unittest.TestCase):

    def test_(self):
        section = Section('')
        self.assertRaises(TypeError, fail_acquire_settings, None,
                          section)
        self.assertRaises(AssertionError,
                          fail_acquire_settings,
                          {'setting': ['description', 'bear']}, section)
        self.assertEqual(fail_acquire_settings({}, section), None,
                         section)
