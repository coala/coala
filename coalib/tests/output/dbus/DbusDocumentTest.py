import sys
import os
import unittest

sys.path.insert(0, ".")
from coalib.output.dbus.DbusDocument import DbusDocument


class DbusDocumentTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
