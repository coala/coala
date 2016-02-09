import unittest

from coalib.settings.Section import Section
from coalib.bears.LocalBear import LocalBear, BEAR_KIND


class LocalBearTest(unittest.TestCase):

    def test_api(self):
        test_object = LocalBear(Section("name"), None)
        self.assertRaises(NotImplementedError,
                          test_object.run,
                          "filename",
                          ["file\n"])

    def test_kind(self):
        self.assertEqual(LocalBear.kind(), BEAR_KIND.LOCAL)


if __name__ == '__main__':
    unittest.main(verbosity=2)
