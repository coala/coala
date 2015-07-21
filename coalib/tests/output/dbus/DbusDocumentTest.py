import sys
import os
import unittest

sys.path.insert(0, ".")
from coalib.output.dbus.DbusDocument import DbusDocument


class DbusDocumentTest(unittest.TestCase):
    def setUp(self):
        self.config_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
            "dbus_test_files",
            ".coafile"))
        self.testcode_c_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
            "dbus_test_files",
            "testcode.c"))

    def test_path(self):
        test_file = "a"
        uut = DbusDocument(doc_id=1)
        self.assertEqual(uut.path, "")

        uut = DbusDocument(doc_id=1, path=test_file)
        self.assertEqual(uut.path, os.path.abspath(test_file))

    def test_config(self):
        uut = DbusDocument(doc_id=1)
        self.assertEqual(uut.FindConfigFile(), "")

        uut.path = self.testcode_c_path
        self.assertEqual(uut.FindConfigFile(), self.config_path)

        uut.SetConfigFile("config_file")
        self.assertEqual(uut.config_file, "config_file")

        self.assertEqual(uut.GetConfigFile(), "config_file")

    def test_analyze(self):
        uut = DbusDocument(doc_id=1)
        self.assertEqual(uut.Analyze(), [])

        uut.path = self.testcode_c_path
        self.assertEqual(uut.Analyze(), [])

        uut.SetConfigFile(self.config_path)
        output = uut.Analyze()
        self.assertEqual(output,
                         ([],
                          [['default',
                           True,
                           [{'debug_msg': '',
                             'file': '',
                             'line_nr': '',
                             'message': 'test msg',
                             'origin': 'LocalTestBear',
                             'severity': 'NORMAL'},
                            {'debug_msg': '',
                             'file': self.testcode_c_path,
                             'line_nr': '',
                             'message': 'test msg',
                             'origin': 'GlobalTestBear',
                             'severity': 'NORMAL'}]]]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
