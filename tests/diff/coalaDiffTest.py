import sys
import os
import unittest
from coalib import coala
from tests.TestUtilities import execute_coala, bear_test_module


class coalaDiffTest(unittest.TestCase):

    def setUp(self):
        self.old_argv = sys.argv

    def tearDown(self):
        sys.argv = self.old_argv

    def test_nonexistent(self):
        retval, stdout, stderr = execute_coala(coala.main, 'coala', '--diff',
                                               '-c', 'nonex')
        self.assertEqual(stdout, '\n')
        self.assertRegex(stderr, ".*Requested coafile '.*' does not exist")
        self.assertNotEqual(retval, 0,
                            'coala must return nonzero when errors occured')

    def test_diff_header(self):
        # test header and change hunks in diff
        with bear_test_module():
            filepath = 'tests/diff/'
            retval, stdout, stderr = execute_coala(coala.main,
                                                   'coala', '--diff',
                                                   '-c', filepath + '.coafile')
            header = ('--- .*testFile.py \n[+]{3} .*testFile.py \n'
                      '@@ [0-9-+, ]+ @@.*')

            self.assertFalse(stderr)
            self.assertRegex(stdout, header)

    def test_changes(self):
        with bear_test_module():
            filepath = 'tests/diff/'
            retval, stdout, stderr = execute_coala(coala.main,
                                                   'coala', '--diff',
                                                   '-c', filepath + '.coafile')
            patch = ('-    return num1 + num2 \n'
                     '+    return num1 + num2')

            self.assertFalse(stderr)
            self.assertIn(patch, stdout)

    def test_output_file(self):
        # test output is written to a file correctly
        filepath = 'tests/diff/'
        retval1, stdout1, stderr1 = execute_coala(coala.main, 'coala', '--diff',
                                                  '-c', filepath + '.coafile')
        retval2, stdout2, stderr2 = execute_coala(coala.main, 'coala', '--diff',
                                                  '-c', filepath + '.coafile',
                                                  '--output',
                                                  filepath + 'diff_file')
        with open(filepath + 'diff_file') as fp:
            data = fp.read()
        os.remove(filepath + 'diff_file')

        self.assertEqual(data + '\n', stdout1)

    def test_output_file_overwriting(self):
        # test output file is overwritten correctly
        filepath = 'tests/diff/'
        with open(filepath + 'diff_file', 'w') as fp:
            fp.write('Winter is Coming')
        fp.close()

        retval1, stdout1, stderr1 = execute_coala(coala.main, 'coala', '--diff',
                                                  '-c', filepath + '.coafile')
        retval2, stdout2, stderr2 = execute_coala(coala.main, 'coala', '--diff',
                                                  '-c', filepath + '.coafile',
                                                  '--output',
                                                  filepath + 'diff_file')
        with open(filepath + 'diff_file') as fp:
            data = fp.read()
        os.remove(filepath + 'diff_file')

        self.assertEqual(data + '\n', stdout1)
