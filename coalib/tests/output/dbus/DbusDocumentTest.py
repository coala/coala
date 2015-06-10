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
        uut = DbusDocument(id=1)
        self.assertEqual(uut.path, "")

        uut = DbusDocument(id=1, path=test_file)
        self.assertEqual(uut.path, os.path.abspath(test_file))

    def test_config(self):
        uut = DbusDocument("dummy_path")
        self.assertEqual(uut.FindConfigFile(), "")

        uut.SetConfigFile("config_file")
        self.assertEqual(uut.config_file, "config_file")

        self.assertEqual(uut.GetConfigFile(), "config_file")

    def test_analyze(self):
        uut = DbusDocument(id=1)
        self.assertEqual(uut.Analyze(), [])

        uut.path = self.testcode_c_path
        self.assertEqual(uut.Analyze(), [])

        uut.SetConfigFile(self.config_path)

        self.assertEqual(uut.Analyze(),
                         [['default',
                           True,
                           [['LocalTestBear',
                             'test msg',
                             'None',
                             'None',
                             '1'],
                            ['GlobalTestBear',
                             'test msg',
                             self.testcode_c_path,
                             'None',
                             '1']]]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
