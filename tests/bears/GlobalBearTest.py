import unittest

from coalib.bears.GlobalBear import BEAR_KIND, GlobalBear
from coalib.settings.Section import Section


class GlobalBearTest(unittest.TestCase):

    def test_api(self):
        test_object = GlobalBear(0, Section('name'), None)
        self.assertRaises(NotImplementedError, test_object.run)

    def test_kind(self):
        self.assertEqual(GlobalBear.kind(), BEAR_KIND.GLOBAL)
