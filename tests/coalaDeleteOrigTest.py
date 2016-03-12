import os
import tempfile
import unittest

from coalib import coala_delete_orig
from coalib.misc.ContextManagers import retrieve_stdout
from coalib.parsing import Globbing
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class coalaDeleteOrigTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("default")
        self.section.append(Setting("config", '/path/to/file'))

    def test_nonexistent_coafile(self):
        old_getcwd = os.getcwd
        os.getcwd = lambda *args: None
        retval = coala_delete_orig.main()
        self.assertEqual(retval, 255)
        os.getcwd = old_getcwd

    def test_remove_exception(self):
        old_glob = Globbing.glob

        # Non existent file
        with retrieve_stdout() as stdout:
            Globbing.glob = lambda *args: ["non_existent_file"]
            retval = coala_delete_orig.main(section=self.section)
            output = stdout.getvalue()
            self.assertEqual(retval, 0)
            self.assertIn("Couldn't delete", output)

        # Directory instead of file
        with tempfile.TemporaryDirectory() as filename, \
                retrieve_stdout() as stdout:
            Globbing.glob = lambda *args: [filename]
            retval = coala_delete_orig.main(section=self.section)
            output = stdout.getvalue()
            self.assertEqual(retval, 0)
            self.assertIn("Couldn't delete", output)

        Globbing.glob = old_glob
