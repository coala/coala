import unittest

from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.bears.GlobalBear import GlobalBear
from coalib.settings.Section import Section


class GlobalBearTest(unittest.TestCase):

    def test_run_raises(self):
        bear = GlobalBear(Section(''), {})
        self.assertRaises(NotImplementedError, bear.run)

    def test_kind(self):
        self.assertEqual(GlobalBear.kind(), BEAR_KIND.GLOBAL)

    def test_api(self):
        test_object = GlobalBear(Section('name'), {})
        self.assertRaises(NotImplementedError, test_object.run)
