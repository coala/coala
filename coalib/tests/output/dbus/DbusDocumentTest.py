import os
import unittest
from unittest.case import skipIf

from coalib.misc import Constants

try:
    from coalib.output.dbus.DbusDocument import DbusDocument
    skip, message = False, ''
except ImportError as err:
    skip, message = True, str(err)


@skipIf(skip, message)
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

        self.maxDiff = None
        uut.SetConfigFile(self.config_path)
        output = uut.Analyze()
        self.assertEqual(output,
                         (1,
                          [],
                          [['default',
                            True,
                            [{'debug_msg': '',
                              'file': '',
                              'id': output[2][0][2][0]['id'],
                              'line_nr': '',
                              'message': 'test msg',
                              'origin': 'LocalTestBear',
                              'severity': 'NORMAL'},
                             {'debug_msg': '',
                              'file': self.testcode_c_path,
                              'id': output[2][0][2][1]['id'],
                              'line_nr': '',
                              'message': 'test msg',
                              'origin': 'GlobalTestBear',
                              'severity': 'NORMAL'}]]]))

        uut.path = "test.unknown_extension"
        output = uut.Analyze()
        self.assertEqual(output, (0, [], []))

        uut.SetConfigFile(self.config_path + "2")
        output = uut.Analyze()
        self.assertEqual(output[0], 255)
        self.assertEqual(output[1][1]["log_level"], "ERROR")
        self.assertEqual(output[1][1]["message"], Constants.CRASH_MESSAGE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
