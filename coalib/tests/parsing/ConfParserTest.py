from collections import OrderedDict
import os
import tempfile
import unittest

from coalib.parsing.ConfParser import ConfParser
from coalib.settings.Section import Section


class ConfParserTest(unittest.TestCase):
    example_file = """to be ignored
    a_default, another = val
    TEST = tobeignored  # do you know that thats a comment
    test = push
    t =
    [MakeFiles]
     j  , another = a
                   multiline
                   value
    # just a omment
    # just a omment
    nokey. = value
    default.test = content
    makefiles.lastone = val

    [EMPTY_ELEM_STRIP]
    A = a, b, c
    B = a, ,, d
    C = ,,,
    """

    def setUp(self):
        self.tempdir = tempfile.gettempdir()
        self.file = os.path.join(self.tempdir, ".coafile")
        self.nonexistentfile = os.path.join(self.tempdir, "e81k7bd98t")
        with open(self.file, "w") as file:
            file.write(self.example_file)

        self.uut = ConfParser()
        try:
            os.remove(self.nonexistentfile)
        except FileNotFoundError:
            pass

        self.sections = self.uut.parse(self.file)

    def tearDown(self):
        os.remove(self.file)

    def test_parse_nonexisting_file(self):
        self.assertRaises(FileNotFoundError,
                          self.uut.parse,
                          self.nonexistentfile)
        self.assertNotEqual(self.uut.parse(self.file, True), self.sections)

    def test_parse_nonexisting_section(self):
        self.assertRaises(IndexError,
                          self.uut.get_section,
                          "inexistent section")

    def test_parse_default_section(self):
        default_should = OrderedDict([
            ('a_default', 'val'),
            ('another', 'val'),
            ('comment0', '# do you know that thats a comment'),
            ('test', 'content'),
            ('t', '')])

        key, val = self.sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'default')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, default_should)

    def test_parse_makefiles_section(self):
        makefiles_should = OrderedDict([
            ('j', 'a\nmultiline\nvalue'),
            ('another', 'a\nmultiline\nvalue'),
            ('comment1', '# just a omment'),
            ('comment2', '# just a omment'),
            ('lastone', 'val'),
            ('comment3', ''),
            ('a_default', 'val'),
            ('comment0', '# do you know that thats a comment'),
            ('test', 'content'),
            ('t', '')])

        # Pop off the default section.
        self.sections.popitem(last=False)

        key, val = self.sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'makefiles')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, makefiles_should)

        self.assertEqual(val["comment1"].key, "comment1")

    def test_parse_empty_elem_strip_section(self):
        empty_elem_strip_should = OrderedDict([
            ('a', 'a, b, c'),
            ('b', 'a, ,, d'),
            ('c', ',,,'),
            ('comment4', ''),
            ('a_default', 'val'),
            ('another', 'val'),
            ('comment0', '# do you know that thats a comment'),
            ('test', 'content'),
            ('t', '')])

        # Pop off the default and makefiles section.
        self.sections.popitem(last=False)
        self.sections.popitem(last=False)

        key, val = self.sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'empty_elem_strip')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, empty_elem_strip_should)

    def test_remove_empty_iter_elements(self):
        # Test with empty-elem stripping.
        uut = ConfParser(remove_empty_iter_elements=True)
        uut.parse(self.file)
        self.assertEqual(list(uut.get_section("EMPTY_ELEM_STRIP")["A"]),
                         ["a", "b", "c"])
        self.assertEqual(list(uut.get_section("EMPTY_ELEM_STRIP")["B"]),
                         ["a", "d"])
        self.assertEqual(list(uut.get_section("EMPTY_ELEM_STRIP")["C"]),
                         [])

        # Test without stripping.
        uut = ConfParser(remove_empty_iter_elements=False)
        uut.parse(self.file)
        self.assertEqual(list(uut.get_section("EMPTY_ELEM_STRIP")["A"]),
                         ["a", "b", "c"])
        self.assertEqual(list(uut.get_section("EMPTY_ELEM_STRIP")["B"]),
                         ["a", "", "", "d"])
        self.assertEqual(list(uut.get_section("EMPTY_ELEM_STRIP")["C"]),
                         ["", "", "", ""])

    def test_config_directory(self):
        self.uut.parse(self.tempdir)

if __name__ == '__main__':
    unittest.main(verbosity=2)
