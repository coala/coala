from collections import OrderedDict
import os
import sys
import tempfile
import unittest

sys.path.insert(0, ".")
from coalib.misc.Compatability import FileNotFoundError
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
        with open(self.file, "w") as filehandler:
            filehandler.write(self.example_file)

        self.uut = ConfParser()
        try:
            os.remove(self.nonexistentfile)
        except FileNotFoundError:
            pass

    def tearDown(self):
        os.remove(self.file)

    def test_parse(self):
        default_should = OrderedDict([
            ('a_default', 'val'),
            ('another', 'val'),
            ('comment0', '# do you know that thats a comment'),
            ('test', 'content'),
            ('t', '')])

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

        self.assertRaises(FileNotFoundError,
                          self.uut.parse,
                          self.nonexistentfile)
        sections = self.uut.parse(self.file)
        self.assertNotEqual(self.uut.parse(self.file, True), sections)

        # Check section "DEFAULT".
        key, val = sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'default')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, default_should)

        # Check section "MakeFiles".
        key, val = sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'makefiles')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, makefiles_should)

        self.assertEqual(val["comment1"].key, "comment1")

        # Check section "EMPTY_ELEM_STRIP".
        key, val = sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'empty_elem_strip')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, empty_elem_strip_should)


        # Check inexistent Section.
        self.assertRaises(IndexError,
                          self.uut.get_section,
                          "inexistent section")

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
