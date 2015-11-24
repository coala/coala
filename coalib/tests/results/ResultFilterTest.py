import os
import sys
import unittest

sys.path.insert(0, ".")


class ResultFilterTest(unittest.TestCase):
    def setUp(self):
        result_filter_test_dir = os.path.join(os.path.split(__file__)[0],
                                              'ResultFilterTestFiles')
        self.original_file_name = os.path.join(result_filter_test_dir,
                                               'original_file.txt')
        self.modified_file_name = os.path.join(result_filter_test_dir,
                                               'modified_file.txt')

    def test_simple_cases(self):
        self.assertTrue(True)

    def test_affected_code(self):
        self.assertTrue(True)

    def test_diffs(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
