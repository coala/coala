from collections import OrderedDict
import re
import os
import unittest

from coalib.settings.Setting import (Setting,
                                     path,
                                     path_list,
                                     typed_list,
                                     typed_dict,
                                     typed_ordered_dict)


class SettingTest(unittest.TestCase):

    def test_construction(self):
        self.assertRaises(ValueError, Setting, "", 2, 2)
        self.assertRaises(TypeError, Setting, "", "", "", from_cli=5)

    def test_path(self):
        self.uut = Setting("key", " 22\n", "." + os.path.sep, True)
        self.assertEqual(path(self.uut),
                         os.path.abspath(os.path.join(".", "22")))

        abspath = os.path.abspath(".")
        self.uut = Setting("key", re.escape(abspath))
        self.assertEqual(path(self.uut), abspath)

        self.uut = Setting("key", " 22", "")
        self.assertRaises(ValueError, path, self.uut)
        self.assertEqual(path(self.uut,
                              origin="test" + os.path.sep),
                         os.path.abspath(os.path.join("test", "22")))

    def test_path_list(self):
        abspath = os.path.abspath(".")
        # Need to escape backslashes since we use list conversion
        self.uut = Setting("key", "., " + abspath.replace("\\", "\\\\"),
                           origin="test" + os.path.sep + "somefile")
        self.assertEqual(path_list(self.uut),
                         [os.path.abspath(os.path.join("test", ".")), abspath])

    def test_typed_list(self):
        self.uut = Setting("key", "1, 2, 3")
        self.assertEqual(typed_list(int)(self.uut),
                         [1, 2, 3])

        with self.assertRaises(ValueError):
            self.uut = Setting("key", "1, a, 3")
            typed_list(int)(self.uut)

    def test_typed_dict(self):
        self.uut = Setting("key", "1, 2: t, 3")
        self.assertEqual(typed_dict(int, str, None)(self.uut),
                         {1: None, 2: "t", 3: None})

        with self.assertRaises(ValueError):
            self.uut = Setting("key", "1, a, 3")
            typed_dict(int, str, "")(self.uut)

    def test_typed_ordered_dict(self):
        self.uut = Setting("key", "1, 2: t, 3")
        self.assertEqual(typed_ordered_dict(int, str, None)(self.uut),
                         OrderedDict([(1, None), (2, "t"), (3, None)]))

        with self.assertRaises(ValueError):
            self.uut = Setting("key", "1, a, 3")
            typed_ordered_dict(int, str, "")(self.uut)

    def test_inherited_conversions(self):
        self.uut = Setting("key", " 22\n", ".", True)
        self.assertEqual(str(self.uut), "22")
        self.assertEqual(int(self.uut), 22)
        self.assertRaises(ValueError, bool, self.uut)


if __name__ == '__main__':
    unittest.main(verbosity=2)
