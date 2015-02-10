from collections import OrderedDict
import os

import sys

sys.path.insert(0, ".")
from coalib.parsing.ConfParser import ConfParser
from coalib.settings.Section import Section
import unittest
import tempfile


class ConfParserTestCase(unittest.TestCase):
    example_file = """to be ignored
    a_default, another = val
    TEST = tobeignored  # do you know that thats a comment
    test = push
    t =
    [MakeFiles]
     j  , another = a
                   multiline
                   value
    ; just a omment
    ; just a omment
    nokey. = value
    default.test = content
    makefiles.lastone = val
    """

    def setUp(self):
        self.file = os.path.join(tempfile.gettempdir(), "ConfParserTestFile")
        self.nonexistentfile = os.path.join(tempfile.gettempdir(), "NonExistentTestFile")
        with open(self.file, "w") as filehandler:
            filehandler.write(self.example_file)

        self.uut = ConfParser()
        if sys.version_info < (3, 3):
            err = OSError
        else:
            err = FileNotFoundError
        try:
            os.remove(self.nonexistentfile)
        except err:
            pass

    def tearDown(self):
        os.remove(self.file)

    def test_parse(self):
        default_should = OrderedDict([
            ('a_default', 'val'),
            ('another', 'val'),
            ('comment0', '# do you know that thats a comment'),
            ('test', 'content'),
            ('t', '')
        ])

        makefiles_should = OrderedDict([
            ('j', 'a\nmultiline\nvalue'),
            ('another', 'a\nmultiline\nvalue'),
            ('comment1', '; just a omment'),
            ('comment2', '; just a omment'),
            ('lastone', 'val'),
            ('comment3', ''),
            ('a_default', 'val'),
            ('comment0', '# do you know that thats a comment'),
            ('test', 'content'),
            ('t', '')
        ])

        self.assertRaises(self.uut.FileNotFoundError, self.uut.parse, self.nonexistentfile)
        sections = self.uut.parse(self.file)
        self.assertNotEqual(self.uut.reparse(self.file), sections)

        key, val = sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'default')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, default_should)

        key, val = sections.popitem(last=False)
        self.assertTrue(isinstance(val, Section))
        self.assertEqual(key, 'makefiles')

        is_dict = OrderedDict()
        for k in val:
            is_dict[k] = str(val[k])
        self.assertEqual(is_dict, makefiles_should)

        self.assertEqual(val["comment1"].key, "comment1")

        self.assertRaises(IndexError, self.uut.get_section, "inexistent section")


if __name__ == '__main__':
    unittest.main(verbosity=2)
