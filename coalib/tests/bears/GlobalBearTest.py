import unittest

from coalib.settings.Section import Section
from coalib.bears.GlobalBear import GlobalBear, BEAR_KIND


class GlobalBearTest(unittest.TestCase):

    def test_api(self):
        test_object = GlobalBear(0, Section("name"), None)
        self.assertRaises(NotImplementedError, test_object.run)

    def test_kind(self):
        self.assertEqual(GlobalBear.kind(), BEAR_KIND.GLOBAL)


if __name__ == '__main__':
    unittest.main(verbosity=2)
