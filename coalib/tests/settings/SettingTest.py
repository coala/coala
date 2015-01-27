import os
import sys
import unittest

sys.path.insert(0, ".")

from coalib.settings.Setting import Setting, path, path_list


class SettingTestCase(unittest.TestCase):
    def test_construction(self):
        self.assertRaises(ValueError, Setting, "", 2, 2)
        self.assertRaises(TypeError, Setting, "", "", "", from_cli=5)

    def test_path(self):
        self.uut = Setting("key", " 22\n", "." + os.path.sep, True)
        self.assertEqual(path(self.uut), os.path.abspath(os.path.join(".", "22")))

        abspath = os.path.abspath(".")
        self.uut = Setting("key", abspath)
        self.assertEqual(path(self.uut), abspath)

        self.uut = Setting("key", " 22", "")
        self.assertRaises(ValueError, path, self.uut)
        self.assertEqual(path(self.uut, origin="test" + os.path.sep), os.path.abspath(os.path.join("test", "22")))

    def test_path_list(self):
        abspath = os.path.abspath(".")
        self.uut = Setting("key", "., " + abspath, origin="test" + os.path.sep + "somefile")
        self.assertEqual(path_list(self.uut), [os.path.abspath(os.path.join("test", ".")), abspath])

    def test_inherited_conversions(self):
        self.uut = Setting("key", " 22\n", ".", True)
        self.assertEqual(str(self.uut), "22")
        self.assertEqual(int(self.uut), 22)
        self.assertRaises(ValueError, bool, self.uut)


if __name__ == '__main__':
    unittest.main(verbosity=2)
