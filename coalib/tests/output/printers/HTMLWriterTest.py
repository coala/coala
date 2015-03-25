import re
import sys
import os
import tempfile

sys.path.insert(0, ".")
from coalib.output.printers.HTMLWriter import HTMLWriter
import unittest


class HTMLWriterTest(unittest.TestCase):
    def setUp(self):
        handle, self.filename = tempfile.mkstemp()
        os.close(handle)  # We don't need the handle provided by mkstemp
        self.uut = HTMLWriter(self.filename)

    def tearDown(self):
        os.remove(self.filename)

    def test_construction(self):
        self.assertRaises(TypeError, HTMLWriter, 5)
        with open(self.filename) as file:
            lines = file.readlines()
        self.assertEqual(lines, [])
        del self.uut

    def test_printing_header_footer(self):
        self.uut = HTMLWriter(self.filename)
        with open(self.filename) as file:
            lines = file.readlines()
        self.assertEqual(lines,
                        ['<!DOCTYPE html>\n',
                         '<html>\n',
                         '</html>\n'])

        del self.uut

    def test_write_comment(self):
        self.uut = HTMLWriter(self.filename)
        self.uut.write_comment("testing comments")
        del self.uut
        with open(self.filename) as file:
            lines = file.readlines()

        self.assertEqual(lines,
                         ['<!DOCTYPE html>\n',
                          '<html>\n',
                          '    <!-- testing comments -->\n',
                          '</html>\n'])

    def test_write_tags(self):
        self.uut = HTMLWriter(self.filename)
        self.tag_dict = {'p':'test'}
        self.uut.write_tags(**self.tag_dict)
        del self.uut

        with open(self.filename) as file:
            lines = file.readlines()

        self.assertEqual(lines,
                         ['<!DOCTYPE html>\n',
                          '<html>\n',
                          '    <p>\n',
                          '        test\n',
                          '    </p>\n',
                          '</html>\n'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
