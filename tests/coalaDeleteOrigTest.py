import tempfile
import unittest

from coalib import coala_delete_orig
from coalib.misc.ContextManagers import retrieve_stdout
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class coalaDeleteOrigTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("default")
        self.section.append(Setting("config", '/path/to/file'))

    @unittest.mock.patch('os.getcwd')
    def test_nonexistent_coafile(self, mocked_getcwd):
        mocked_getcwd.return_value = None
        retval = coala_delete_orig.main()
        self.assertEqual(retval, 255)

    @unittest.mock.patch('coalib.parsing.Globbing.glob')
    def test_remove_exception(self, mock_glob):
        # Non existent file
        mock_glob.return_value = ["non_existent_file"]
        with retrieve_stdout() as stdout:
            retval = coala_delete_orig.main(section=self.section)
            output = stdout.getvalue()
            self.assertEqual(retval, 0)
            self.assertIn("Couldn't delete", output)

        # Directory instead of file
        with tempfile.TemporaryDirectory() as filename, \
                retrieve_stdout() as stdout:
            mock_glob.return_value = [filename]
            retval = coala_delete_orig.main(section=self.section)
            output = stdout.getvalue()
            self.assertEqual(retval, 0)
            self.assertIn("Couldn't delete", output)
