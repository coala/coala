import unittest

from coalib.misc.StringConverter import StringConverter


class StringConverterTest(unittest.TestCase):

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

    def test_float_conversion(self):
        self.assertEqual(float(self.uut), 1)
        self.uut.value = "0.5 "
        self.assertEqual(float(self.uut), 0.5)
        self.uut = StringConverter(" not a float ")
        self.assertRaises(ValueError, float, self.uut)

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
                         ["a", "test", "with", "some", "\\ challenge "])
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

        uut = StringConverter("A,B,C  ,  D\\x \\a,42,\\n8 ",
                              strip_whitespaces=False)
        self.assertEqual(list(uut), ["A", "B", "C  ", "  Dx a", "42", "n8 "])

    def test_iterator_escape_whitespaces(self):
        uut = StringConverter("ta, chi, tsu, te, \\ to", list_delimiters=",")
        self.assertEqual(list(uut), ["ta", "chi", "tsu", "te", " to"])

        uut = StringConverter(r"/**, \ *\ , \ */", list_delimiters=",")
        self.assertEqual(list(uut), ["/**", " * ", " */"])

        uut = StringConverter(
            "abc\\\\ , def\\ \\ \\ ,   \\\\ unstrip \\\\\\  ",
            list_delimiters=",")
        self.assertEqual(list(uut), ["abc\\", "def   ", "\\ unstrip \\ "])

    def test_iterator_remove_empty_iter_elements(self):
        uut = StringConverter("a, b, c, , e, , g", list_delimiters=",")
        self.assertEqual(list(uut), ["a", "b", "c", "e", "g"])

        uut = StringConverter("a, , ,, e, , g",
                              list_delimiters=",",
                              remove_empty_iter_elements=True)
        self.assertEqual(list(uut), ["a", "e", "g"])

        uut = StringConverter(",,, ,",
                              list_delimiters=",",
                              remove_empty_iter_elements=True)
        self.assertEqual(list(uut), [])

        uut = StringConverter("a, b, c, , e, , g",
                              list_delimiters=",",
                              remove_empty_iter_elements=False)
        self.assertEqual(list(uut), ["a", "b", "c", "", "e", "", "g"])

        uut = StringConverter(",,, ,",
                              list_delimiters=",",
                              remove_empty_iter_elements=False)
        self.assertEqual(list(uut), ["", "", "", "", ""])

    def test_dict_escape_whitespaces(self):
        uut = StringConverter(
            "\\  : \\  , hello: \\ world, \\\\ A \\\\ : B\\ ")
        self.assertEqual(dict(uut), {" ": " ",
                                     "hello": " world",
                                     "\\ A \\": "B "})

        uut = StringConverter(r"/**, \ *\ , \ */")
        self.assertEqual(dict(uut), {"/**": "", " * ": "", " */": ""})

        uut = StringConverter("abc\\\\  :    qew, def\\ \\ \\ ,"
                              "   \\\\ unstrip \\\\\\  ")
        self.assertEqual(dict(uut), {"abc\\": "qew",
                                     "def   ": "",
                                     "\\ unstrip \\ ": ""})

        uut = StringConverter("A:B,C  :  D\\x \\a,42:\\n8 ",
                              strip_whitespaces=False)
        self.assertEqual(dict(uut), {"A": "B", "C  ": "  Dx a", "42": "n8 "})

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
