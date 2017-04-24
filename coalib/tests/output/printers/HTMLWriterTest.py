import re
import sys
import os
import tempfile
import unittest
import collections

sys.path.insert(0, ".")
from coalib.output.printers.HTMLWriter import HTMLWriter


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

    def test_printing_header_footer(self):
        del self.uut
        with open(self.filename) as file:
            lines = file.readlines()
            self.assertEqual(lines,
                         ['<!DOCTYPE html>\n',
                          '<html>\n',
                          '</html>\n'])

    def test_write_comment(self):
        # Test for single comment
        self.uut.write_comment("testing comments")
        del self.uut
        with open(self.filename) as file:
            lines = file.readlines()

            self.assertEqual(lines,
                         ['<!DOCTYPE html>\n',
                          '<html>\n',
                          '    <!-- testing comments -->\n',
                          '</html>\n'])

        # Test for multiple comments
        self.uut = HTMLWriter(self.filename)
        self.uut.write_comment("test1")
        self.uut.write_comment("test2")
        del self.uut
        with open(self.filename) as file:
            lines = file.readlines()

            self.assertEqual(lines,
                         ['<!DOCTYPE html>\n',
                          '<html>\n',
                          '    <!-- test1 -->\n',
                          '    <!-- test2 -->\n',
                          '</html>\n'])

        # Test for no comments
        self.uut = HTMLWriter(self.filename)
        self.uut.write_comment()
        del self.uut
        with open(self.filename) as file:
            lines = file.readlines()

            self.assertEqual(lines,
                         ['<!DOCTYPE html>\n',
                          '<html>\n',
                          '</html>\n'])

    def test_write_tag(self):
        self.tag = "p"
        self.content = "test"
        self.uut.write_tag(self.tag, self.content, style="color:Yellow")
        del self.uut

        with open(self.filename) as file:
            lines = file.readlines()

            self.assertEqual(lines,
                         ['<!DOCTYPE html>\n',
                          '<html>\n',
                          '    <p style="color:Yellow">\n',
                          '        test\n',
                          '    </p>\n',
                          '</html>\n'])

        self.uut = HTMLWriter(self.filename)
        self.tag = "br"
        self.content = ""
        self.uut.write_tag(self.tag, self.content)
        del self.uut

        with open(self.filename) as file:
            lines = file.readlines()

            self.assertEqual(lines,
                         ['<!DOCTYPE html>\n',
                          '<html>\n',
                          '    <br/>\n',
                          '</html>\n'])

if __name__ == '__main__':
    unittest.main(verbosity=2)
