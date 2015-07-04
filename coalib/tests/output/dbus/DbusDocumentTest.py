import sys
import os
import unittest

sys.path.insert(0, ".")
from coalib.output.dbus.DbusDocument import DbusDocument
from coalib.misc.ContextManagers import retrieve_stdout


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
        uut = DbusDocument(id=1)
        self.assertEqual(uut.FindConfigFile(), "")

        uut.path = self.testcode_c_path
        self.assertEqual(uut.FindConfigFile(), self.config_path)

        uut.SetConfigFile("config_file")
        self.assertEqual(uut.config_file, "config_file")

        self.assertEqual(uut.GetConfigFile(), "config_file")

        uut.verbose = True

        with retrieve_stdout() as stdout:
            uut.FindConfigFile()
            expected_output = ('DbusDocument:FindConfigFile - found ' +
                               self.config_path + '\n')
            self.assertEqual(expected_output, stdout.getvalue())

            uut.SetConfigFile("config_file")
            expected_output += ('DbusDocument:SetConfigFile - set to '
                                'config_file\n')
            self.assertEqual(expected_output, stdout.getvalue())

            uut.GetConfigFile()
            expected_output += 'DbusDocument:GetConfigFile - got config_file\n'
            self.assertEqual(expected_output, stdout.getvalue())

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
                             '1']]],
                           ['c2',
                            False,
                            []]])

        uut.verbose = True
        a = None
        with retrieve_stdout() as stdout:
            uut.path = ""
            uut.Analyze()
            expected_output = ('DbusDocument:Analyze - empty because '
                               'path is empty\n')
            self.assertEqual(expected_output, stdout.getvalue())

            uut.config_file = ""
            uut.Analyze()
            expected_output += ('DbusDocument:Analyze - empty because '
                                'config_file is empty and path is empty\n')
            self.assertEqual(expected_output, stdout.getvalue())

            uut.path = self.testcode_c_path
            uut.Analyze()
            expected_output += ('DbusDocument:Analyze - empty because '
                                'config_file is empty\n')
            self.assertEqual(expected_output, stdout.getvalue())

            uut.SetConfigFile(self.config_path)
            expected_output = stdout.getvalue()

            uut.Analyze()
            expected_output += (
'''DbusDocument:Analyze - section default results:
  string  section default
  boolean result True
  struct result:
    string origin LocalTestBear
    string message test msg
    string file None
    string line_nr None
    string severity 1
  struct result:
    string origin GlobalTestBear
    string message test msg
    string file %s
    string line_nr None
    string severity 1
DbusDocument:Analyze - section c not enabled
DbusDocument:Analyze - section c2 results:
  string  section c2
  boolean result False
  struct result: empty
----------------------------------------------------------------------
''' % (self.testcode_c_path))
            self.maxDiff = None
            self.assertEqual(expected_output, stdout.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
