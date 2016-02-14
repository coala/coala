import sys
import os
import unittest
import re
from coalib import coala_format
from coalib.tests.TestUtilities import execute_coala
from tempfile import TemporaryDirectory, NamedTemporaryFile
from coalib.misc.ContextManagers import make_temp


class coalaFormatTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv
        self.unescaped_coafile = os.path.abspath("./.coafile")
        self.coafile = re.escape(self.unescaped_coafile)

    def tearDown(self):
        sys.argv = self.old_argv

    def test_nonexistent(self):
        retval, output = execute_coala(
            coala_format.main, "coala-format", "-c", 'nonex', "test")
        self.assertRegex(
            output, "The requested coafile '.*' does not exist.")

    def test_find_issues(self):
        retval, output = execute_coala(
            coala_format.main, "coala-format", "todos", "-c",
            self.coafile)
        self.assertRegex(output,
                         r'msg:The line contains the keyword `# \w+`.',
                         "coala-format output should be empty when running "
                         "over its own code. (Target section: todos)")
        self.assertNotEqual(retval,
                            0,
                            "coala-format must return nonzero when running "
                            "over its own code. (Target section: todos)")

    def test_fail_acquire_settings(self):
        retval, output = execute_coala(coala_format.main,
                                       "coala-ci",
                                       "-b",
                                       'SpaceConsistencyBear',
                                       '-c',
                                       os.devnull)
        self.assertIn("During execution, we found that some", output)

    def test_coala_delete_orig(self):
        with TemporaryDirectory() as tempdir,\
             NamedTemporaryFile(suffix='.orig',
                                dir=tempdir,
                                delete=False) as orig_file,\
             make_temp(suffix='.coafile', prefix='', dir=tempdir) as coafile,\
             make_temp(dir=tempdir) as unrelated_file:
            orig_file.close()
            execute_coala(coala_format.main, "coala-format",
                          "-c", re.escape(coafile))
            self.assertFalse(os.path.isfile(orig_file.name))
            self.assertTrue(os.path.isfile(unrelated_file))
