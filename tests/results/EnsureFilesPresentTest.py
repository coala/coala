import unittest
from os.path import abspath

from coalib.results.ResultFilter import ensure_files_present


class EnsureFilesPresentTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_removed_file(self):
        test_file = ['abc']
        test_file_dict = {'test_file': test_file}
        test_mod_file_dict = {}

        ensure_files_present(test_file_dict, test_mod_file_dict)

        self.assertEqual(
            test_mod_file_dict,
            {'test_file': []})

    def test_added_file(self):
        test_file = ['abc']
        test_file_dict = {}
        test_mod_file_dict = {'test_file': test_file}

        ensure_files_present(test_file_dict, test_mod_file_dict)

        self.assertEqual(
            test_file_dict,
            {'test_file': []})

    def test_file_renaming(self):
        testfile_1 = ['1\n', '2\n']
        testfile_2 = ['3\n', '4\n', '5\n']

        tf1 = abspath('tf1')
        tf2 = abspath('tf2')
        tf1_new = abspath('tf1_new')

        original_file_dict = {tf1: testfile_1, tf2: testfile_2}
        modified_file_dict = {tf1_new: testfile_1}

        renamed_files = ensure_files_present(original_file_dict,
                                             modified_file_dict)

        self.assertEqual({tf1: tf1_new}, renamed_files)

    def test_file_deletion(self):
        testfile_1 = ['1\n', '2\n']
        testfile_2 = ['3\n', '4\n', '5\n']

        tf1 = abspath('tf1')
        tf2 = abspath('tf2')

        original_file_dict = {tf1: testfile_1, tf2: testfile_2}
        modified_file_dict = {tf1: testfile_1}

        renamed_files = ensure_files_present(original_file_dict,
                                             modified_file_dict)

        self.assertEqual({}, renamed_files)

    def test_file_renaming_changed_file(self):
        testfile_1 = ['1\n', '2\n']
        testfile_2 = ['3\n', '4\n', '5\n']

        tf1 = abspath('tf1')
        tf2 = abspath('tf2')

        testfile_2_new = ['6\n', '4\n', '5\n']
        tf2_new = abspath('tf2_new')

        original_file_dict = {tf1: testfile_1, tf2: testfile_2}
        modified_file_dict = {tf2_new: testfile_2_new}

        renamed_files = ensure_files_present(original_file_dict,
                                             modified_file_dict)

        self.assertEqual({tf2: tf2_new}, renamed_files)

    def test_file_addition_deletion_similar_files(self):
        testfile_1 = ['1\n', '2\n']
        testfile_2 = ['3\n', '4\n', '5\n']

        tf1 = abspath('tf1')
        tf2 = abspath('tf2')

        testfile_2_new = ['3\n']
        tf2_new = abspath('tf2_new')

        original_file_dict = {tf1: testfile_1, tf2: testfile_2}
        modified_file_dict = {tf2_new: testfile_2_new}

        renamed_files = ensure_files_present(original_file_dict,
                                             modified_file_dict)

        self.assertEqual({}, renamed_files)

        testfile_1 = ['1\n', '2\n']
        testfile_2 = ['3\n', '4\n', '5\n']

        tf1 = abspath('tf1')
        tf2 = abspath('tf2')

        testfile_2_new = ['1\n', '2\n', '0\n', '1\n', '2\n', '1\n', '2\n']
        tf2_new = abspath('tf2_new')

        original_file_dict = {tf1: testfile_1, tf2: testfile_2}
        modified_file_dict = {tf2_new: testfile_2_new}

        renamed_files = ensure_files_present(original_file_dict,
                                             modified_file_dict)

        self.assertEqual({}, renamed_files)
