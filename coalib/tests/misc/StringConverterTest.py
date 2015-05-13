import sys

sys.path.insert(0, ".")
from coalib.misc.StringConverter import StringConverter
import unittest


class ProcessTest(unittest.TestCase):
    def setUp(self):
        self.uut = StringConverter("\n \\1 \n ")

    def test_construction(self):
        self.assertRaises(TypeError,
                          StringConverter,
                          "test",
                          strip_whitespaces=5)
        self.assertRaises(TypeError,
                          StringConverter,
                          "test",
                          list_delimiters=5)

    def test_whitespace_stripping(self):
        self.assertEqual(str(self.uut), "1")

        self.uut = StringConverter("\n 1 \n", strip_whitespaces=False)
        self.assertEqual(str(self.uut), "\n 1 \n")

    def test_int_conversion(self):
        self.assertEqual(int(self.uut), 1)
        self.uut = StringConverter(" not an int ")
        self.assertRaises(ValueError, int, self.uut)

    def test_len(self):
        self.assertEqual(len(self.uut), 1)

    def test_iterator(self):
        self.uut = StringConverter("a, test with!!some challenge",
                                   list_delimiters=[",", " ", "!!"])
        self.assertEqual(list(self.uut),
                         ["a", "test", "with", "some", "challenge"])
        self.uut = StringConverter("a\\ \\,\\\\ test with!!some challenge",
                                   list_delimiters=[",", " ", "!!"])
        self.assertEqual(list(self.uut),
                         ["a ,\\", "test", "with", "some", "challenge"])
        self.uut = StringConverter("a, test with!some \\\\\\ challenge\\ ",
                                   list_delimiters=", !",
                                   strip_whitespaces=False)
        self.assertEqual(list(self.uut),
                         ["a", "test", "with", "some", "\\ challenge "])
        self.uut = StringConverter("a, test with!some \\\\\\ challenge\\ ",
                                   list_delimiters=", !",
                                   strip_whitespaces=True)
        self.assertEqual(list(self.uut),
                         ["a", "test", "with", "some", "\\ challenge"])
        self.uut = StringConverter("testval", list_delimiters=[",", "¸"])
        self.uut.value = "a\\n,bug¸g"
        self.assertEqual(list(self.uut), ["an", "bug", "g"])
        self.assertEqual(list(self.uut.__iter__(False)), ["a\\n", "bug", "g"])

        self.assertTrue("bug" in self.uut)
        self.assertFalse("but" in self.uut)

        self.uut = StringConverter("a, test, \n",
                                   list_delimiters=[","],
                                   strip_whitespaces=True)
        self.assertEqual(list(self.uut), ["a", "test"])
        self.uut = StringConverter("a, test, \n",
                                   list_delimiters=[","],
                                   strip_whitespaces=False)
        self.assertEqual(list(self.uut), ["a", " test", " \n"])

    def test_dict_conversion(self):
        self.uut = StringConverter("test")
        self.assertEqual(dict(self.uut), {"test": ""})
        self.uut = StringConverter("test, t")
        self.assertEqual(dict(self.uut), {"test": "", "t": ""})
        self.uut = StringConverter("test, t: v")
        self.assertEqual(dict(self.uut), {"test": "", "t": "v"})

        # Check escaping
        self.uut = StringConverter("test, t\\: v")
        self.assertEqual(dict(self.uut), {"test": "", "t: v": ""})
        self.uut = StringConverter("test, t\\: v: t")
        self.assertEqual(dict(self.uut), {"test": "", "t: v": "t"})
        self.uut = StringConverter("test\\, t\\: v: t")
        self.assertEqual(dict(self.uut), {"test, t: v": "t"})
        self.uut = StringConverter("test\\, t\\: v: t\\,")
        self.assertEqual(dict(self.uut), {"test, t: v": "t,"})

        # Check that lists ignore colons
        self.assertEqual(list(self.uut), ["test, t: v: t,"])

    def test_bool_conversion(self):
        self.assertEqual(bool(self.uut), True)
        self.uut.value = "yeah"
        self.assertEqual(bool(self.uut), True)
        self.uut = StringConverter("y")
        self.assertEqual(bool(self.uut), True)
        self.uut = StringConverter("nope")
        self.assertEqual(bool(self.uut), False)

        self.uut = StringConverter(" i dont know ")
        self.assertRaises(ValueError, bool, self.uut)

    def test_equality_comparision(self):
        self.assertEqual(StringConverter(" i dont know "),
                         StringConverter("i dont know"))
        self.assertNotEqual(StringConverter(" dont know "),
                            StringConverter("i dont know "))
        self.assertNotEqual(StringConverter(""),
                            StringConverter("i dont know "))
        self.assertNotEqual(5, StringConverter("i dont know "))


if __name__ == '__main__':
    unittest.main(verbosity=2)
