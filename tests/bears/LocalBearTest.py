import unittest

from coalib.bears.LocalBear import BEAR_KIND, LocalBear
from coalib.settings.Section import Section


class LocalBearTest(unittest.TestCase):

    def test_api(self):
        test_object = LocalBear(Section('name'), None)
        self.assertRaises(NotImplementedError,
                          test_object.run,
                          'filename',
                          ['file\n'])

    def test_kind(self):
        self.assertEqual(LocalBear.kind(), BEAR_KIND.LOCAL)
