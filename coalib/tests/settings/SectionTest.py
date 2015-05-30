import unittest
import sys

sys.path.insert(0, ".")

from coalib.settings.Section import Section, Setting, append_to_sections
from coalib.misc.StringConstants import StringConstants


class SectionTest(unittest.TestCase):
    def test_construction(self):
        uut = Section(StringConstants.COMPLEX_TEST_STRING, None)
        uut = Section(StringConstants.COMPLEX_TEST_STRING, uut)
        self.assertRaises(TypeError, Section, "irrelevant", 5)
        self.assertRaises(ValueError, uut.__init__, "name", uut)

    def test_append(self):
        uut = Section(StringConstants.COMPLEX_TEST_STRING, None)
        self.assertRaises(TypeError, uut.append, 5)
        uut.append(Setting(5, 5, 5))
        self.assertEqual(str(uut.get("5 ")), "5")
        self.assertEqual(int(uut.get("nonexistent", 5)), 5)

    def test_enabled(self):
        uut = Section("name")
        self.assertTrue(uut.is_enabled([]))
        self.assertTrue(uut.is_enabled(["name", "wrongname"]))
        self.assertFalse(uut.is_enabled(["wrongname"]))

        uut.append(Setting("enabled", "false"))
        self.assertFalse(uut.is_enabled([]))
        self.assertFalse(uut.is_enabled(["wrong_name"]))
        self.assertTrue(uut.is_enabled(["name", "wrongname"]))

    def test_iter(self):
        defaults = Section("default", None)
        uut = Section("name", defaults)
        uut.append(Setting(5, 5, 5))
        uut.add_or_create_setting(Setting("TEsT", 4, 5))
        defaults.append(Setting("tEsT", 1, 3))
        defaults.append(Setting(" great   ", 3, 8))
        defaults.append(Setting(" great   ", 3, 8), custom_key="custom")
        uut.add_or_create_setting(Setting(" NEW   ", "val", 8))
        uut.add_or_create_setting(Setting(" NEW   ", "vl", 8),
                                  allow_appending=False)
        uut.add_or_create_setting(Setting("new", "val", 9),
                                   custom_key="teSt ",
                                   allow_appending=True)
        self.assertEqual(list(uut), ["5", "test", "new", "great", "custom"])

        for index in uut:
            t = uut[index]
            self.assertNotEqual(t, None)

        self.assertEqual(True, "teST" in defaults)
        self.assertEqual(True, "       GREAT" in defaults)
        self.assertEqual(False, "       GrEAT !" in defaults)
        self.assertEqual(False, "" in defaults)
        self.assertEqual(str(uut['test']), "4\nval")
        self.assertEqual(int(uut["GREAT "]), 3)
        self.assertRaises(IndexError, uut.__getitem__, "doesnotexist")
        self.assertRaises(IndexError, uut.__getitem__, "great", True)
        self.assertRaises(IndexError, uut.__getitem__, " ")

    def test_string_conversion(self):
        uut = Section("name")
        self.assertEqual(str(uut), "name {}")
        uut.append(Setting("key", "value"))
        self.assertEqual(str(uut), "name {key : value}")
        uut.append(Setting("another_key", "another_value"))
        self.assertEqual(str(uut),
                         "name {key : value, another_key : another_value}")

    def test_copy(self):
        uut = Section("name")
        uut.append(Setting("key", "value"))
        self.assertEqual(str(uut["key"]), "value")
        copy = uut.copy()
        self.assertEqual(str(copy), str(uut))
        uut.append(Setting("key", "another_value"))
        self.assertNotEqual(str(copy), str(uut))

        uut.defaults = copy
        copy = uut.copy()
        self.assertEqual(str(uut.defaults), str(copy.defaults))
        uut.defaults.append(Setting("key", "quite_something_else"))
        self.assertNotEqual(str(uut.defaults), str(copy.defaults))

    def test_update(self):
        cli = Section("cli", None)
        conf = Section("conf", None)

        self.assertRaises(TypeError, cli.update, 4)

        cli.append(Setting("key1", "value11"))
        cli.append(Setting("key2", "value12"))
        conf.append(Setting("key1", "value21"))
        conf.append(Setting("key3", "value23"))

        # Values are overwritten, new keys appended
        self.assertEqual(str(conf.copy().update(cli)),
                         "conf {key1 : value11, key3 : value23, "
                         "key2 : value12}")

        cli.defaults = Section("clidef", None)
        cli.defaults.append(Setting("def1", "dval1"))

        self.assertEqual(str(conf.copy().update(cli).defaults),
                         "clidef {def1 : dval1}")

        conf.defaults = Section("confdef", None)
        conf.defaults.append(Setting("def2", "dval2"))

        self.assertEqual(str(conf.copy().update(cli).defaults),
                         "confdef {def2 : dval2, def1 : dval1}")

    def test_append_to_sections(self):
        sections = {}

        append_to_sections(sections, "", "", "")
        self.assertEqual(sections, {})

        append_to_sections(sections, "key", None, "")
        self.assertEqual(sections, {})

        append_to_sections(sections, "test", "val", "origin")
        self.assertIn("default", sections)
        self.assertEqual(len(sections), 1)
        self.assertEqual(len(sections["default"].contents), 1)

        append_to_sections(sections, "test1", "val", "origin", "default")
        self.assertIn("default", sections)
        self.assertEqual(len(sections), 1)
        self.assertEqual(len(sections["default"].contents), 2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
