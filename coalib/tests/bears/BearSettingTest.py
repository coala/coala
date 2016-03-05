import unittest

from coalib.bears.BearSetting import BearSetting


class BearSettingTest(unittest.TestCase):

    def test_properties(self):
        uut = BearSetting("name", "desc", str)
        self.assertEqual(uut.name, "name")
        self.assertEqual(uut.description, "desc")
        self.assertIs(uut.type, str)
        self.assertIsNone(uut.default)

        uut = BearSetting("name2", "2desc", int, 42)
        self.assertEqual(uut.name, "name2")
        self.assertEqual(uut.description, "2desc")
        self.assertIs(uut.type, int)
        self.assertEqual(uut.default, 42)
