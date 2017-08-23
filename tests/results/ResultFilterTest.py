import os
import unittest
from os.path import abspath

from coalib.results.Diff import Diff
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.results.ResultFilter import (
    filter_results,
    remove_range,
    remove_result_ranges_diffs)
from coalib.results.SourceRange import SourceRange


class ResultFilterTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        result_filter_test_dir = os.path.join(os.path.split(__file__)[0],
                                              'ResultFilterTestFiles')
        self.original_file_name = os.path.join(result_filter_test_dir,
                                               'original_file.txt')
        self.modified_file_name = os.path.join(result_filter_test_dir,
                                               'modified_file.txt')

    def test_simple_cases(self):
        class Origin:
            pass

        origin_instance = Origin()

        original_result = Result.from_values(origin=origin_instance,
                                             message='original',
                                             file='original',
                                             severity=RESULT_SEVERITY.NORMAL,
                                             debug_msg='original')

        clone_result = Result.from_values(origin='Origin',
                                          message='original',
                                          file='original',
                                          severity=RESULT_SEVERITY.NORMAL,
                                          debug_msg='original')

        wrong_origin_result = Result.from_values(
            origin='AnotherOrigin',
            message='original',
            file='original',
            severity=RESULT_SEVERITY.NORMAL,
            debug_msg='original')

        wrong_message_result = Result.from_values(
            origin='Origin',
            message='another message',
            file='original',
            severity=RESULT_SEVERITY.NORMAL,
            debug_msg='original')

        wrong_severity_result = Result.from_values(
            origin='Origin',
            message='original',
            file='original',
            severity=RESULT_SEVERITY.INFO,
            debug_msg='original')

        wrong_debug_msg_result = Result.from_values(
            origin='Origin',
            message='original',
            file='original',
            severity=RESULT_SEVERITY.NORMAL,
            debug_msg='another debug message')

        file_dict = {abspath('original'): []}

        self.assertEqual(sorted(filter_results(original_file_dict=file_dict,
                                               modified_file_dict=file_dict,
                                               original_results=[
                                                   original_result],
                                               modified_results=[
                                                   clone_result,
                                                   wrong_origin_result,
                                                   wrong_message_result,
                                                   wrong_severity_result,
                                                   wrong_debug_msg_result])),
                         sorted([wrong_origin_result,
                                 wrong_message_result,
                                 wrong_severity_result,
                                 wrong_debug_msg_result]))

    def test_affected_code(self):

        # ORIGINAL SOURCE RANGES:
        sr0_pre_change = SourceRange.from_values('file_name',
                                                 start_line=4,
                                                 start_column=1,
                                                 end_line=4,
                                                 end_column=6)
        sr0_change = SourceRange.from_values('file_name',
                                             start_line=4,
                                             start_column=8,
                                             end_line=4,
                                             end_column=13)
        sr0_post_change = SourceRange.from_values('file_name',
                                                  start_line=4,
                                                  start_column=15,
                                                  end_line=4,
                                                  end_column=19)

        sr0_pre_remove = SourceRange.from_values('file_name',
                                                 start_line=6,
                                                 start_column=1,
                                                 end_line=6,
                                                 end_column=6)
        sr0_post_remove = SourceRange.from_values('file_name',
                                                  start_line=8,
                                                  start_column=1,
                                                  end_line=8,
                                                  end_column=5)

        sr0_pre_addition = SourceRange.from_values('file_name',
                                                   start_line=10,
                                                   start_column=1,
                                                   end_line=10,
                                                   end_column=6)
        sr0_post_addition = SourceRange.from_values('file_name',
                                                    start_line=11,
                                                    start_column=1,
                                                    end_line=11,
                                                    end_column=5)

        # ORIGINAL RESULTS:
        res0_pre_change = Result(origin='origin',
                                 message='message',
                                 affected_code=(sr0_pre_change,))
        res0_change = Result(origin='origin',
                             message='message',
                             affected_code=(sr0_change,))
        res0_post_change = Result(origin='origin',
                                  message='message',
                                  affected_code=(sr0_post_change,))
        res0_around_change = Result(origin='origin',
                                    message='message',
                                    affected_code=(sr0_pre_change,
                                                   sr0_post_change))
        res0_with_change = Result(origin='origin',
                                  message='message',
                                  affected_code=(sr0_pre_change,
                                                 sr0_change,
                                                 sr0_post_change))
        res0_whole_change = Result.from_values(origin='origin',
                                               message='message',
                                               file='file_name',
                                               line=4,
                                               column=1,
                                               end_line=4,
                                               end_column=19)

        res0_pre_remove = Result(origin='origin',
                                 message='message',
                                 affected_code=(sr0_pre_remove,))
        res0_post_remove = Result(origin='origin',
                                  message='message',
                                  affected_code=(sr0_post_remove,))
        res0_around_remove = Result(origin='origin',
                                    message='message',
                                    affected_code=(sr0_pre_remove,
                                                   sr0_post_remove))
        res0_whole_remove = Result.from_values(origin='origin',
                                               message='message',
                                               file='file_name',
                                               line=6,
                                               column=1,
                                               end_line=8,
                                               end_column=5)

        res0_pre_addition = Result(origin='origin',
                                   message='message',
                                   affected_code=(sr0_pre_addition,))
        res0_post_addition = Result(origin='origin',
                                    message='message',
                                    affected_code=(sr0_post_addition,))
        res0_around_addition = Result(origin='origin',
                                      message='message',
                                      affected_code=(sr0_pre_addition,
                                                     sr0_post_addition))
        res0_whole_addition = Result.from_values(origin='origin',
                                                 message='message',
                                                 file='file_name',
                                                 line=10,
                                                 column=1,
                                                 end_line=11,
                                                 end_column=5)

        # NEW SOURCE RANGES:
        sr1_pre_change = SourceRange.from_values('file_name',
                                                 start_line=4,
                                                 start_column=1,
                                                 end_line=4,
                                                 end_column=6)
        sr1_change = SourceRange.from_values('file_name',
                                             start_line=4,
                                             start_column=8,
                                             end_line=4,
                                             end_column=13)
        sr1_post_change = SourceRange.from_values('file_name',
                                                  start_line=4,
                                                  start_column=15,
                                                  end_line=4,
                                                  end_column=19)

        sr1_pre_remove = SourceRange.from_values('file_name',
                                                 start_line=6,
                                                 start_column=1,
                                                 end_line=6,
                                                 end_column=6)
        sr1_post_remove = SourceRange.from_values('file_name',
                                                  start_line=7,
                                                  start_column=1,
                                                  end_line=7,
                                                  end_column=5)

        sr1_pre_addition = SourceRange.from_values('file_name',
                                                   start_line=9,
                                                   start_column=1,
                                                   end_line=9,
                                                   end_column=6)
        sr1_addition = SourceRange.from_values('file_name',
                                               start_line=10,
                                               start_column=1,
                                               end_line=10,
                                               end_column=8)
        sr1_post_addition = SourceRange.from_values('file_name',
                                                    start_line=11,
                                                    start_column=1,
                                                    end_line=11,
                                                    end_column=5)

        # NEW RESULTS:
        res1_pre_change = Result(origin='origin',
                                 message='message',
                                 affected_code=(sr1_pre_change,))
        res1_change = Result(origin='origin',
                             message='message',
                             affected_code=(sr1_change,))
        res1_post_change = Result(origin='origin',
                                  message='message',
                                  affected_code=(sr1_post_change,))
        res1_around_change = Result(origin='origin',
                                    message='message',
                                    affected_code=(sr1_pre_change,
                                                   sr1_post_change))
        res1_with_change = Result(origin='origin',
                                  message='message',
                                  affected_code=(sr1_pre_change,
                                                 sr1_change,
                                                 sr1_post_change))
        res1_whole_change = Result.from_values(origin='origin',
                                               message='message',
                                               file='file_name',
                                               line=4,
                                               column=1,
                                               end_line=4,
                                               end_column=19)

        res1_pre_remove = Result(origin='origin',
                                 message='message',
                                 affected_code=(sr1_pre_remove,))
        res1_post_remove = Result(origin='origin',
                                  message='message',
                                  affected_code=(sr1_post_remove,))
        res1_around_remove = Result(origin='origin',
                                    message='message',
                                    affected_code=(sr1_pre_remove,
                                                   sr1_post_remove))
        res1_whole_remove = Result.from_values(origin='origin',
                                               message='message',
                                               file='file_name',
                                               line=6,
                                               column=1,
                                               end_line=7,
                                               end_column=5)

        res1_pre_addition = Result(origin='origin',
                                   message='message',
                                   affected_code=(sr1_pre_addition,))
        res1_addition = Result(origin='origin',
                               message='message',
                               affected_code=(sr1_addition,))
        res1_post_addition = Result(origin='origin',
                                    message='message',
                                    affected_code=(sr1_post_addition,))
        res1_around_addition = Result(origin='origin',
                                      message='message',
                                      affected_code=(sr1_pre_addition,
                                                     sr1_post_addition))
        res1_with_addition = Result(origin='origin',
                                    message='message',
                                    affected_code=(sr1_pre_addition,
                                                   sr1_addition,
                                                   sr1_post_addition))
        res1_whole_addition = Result.from_values(origin='origin',
                                                 message='message',
                                                 file='file_name',
                                                 line=9,
                                                 column=1,
                                                 end_line=11,
                                                 end_column=5)

        original_result_list = [res0_pre_change,
                                res0_change,
                                res0_post_change,
                                res0_around_change,
                                res0_with_change,
                                res0_whole_change,

                                res0_pre_remove,
                                res0_post_remove,
                                res0_around_remove,
                                res0_whole_remove,

                                res0_pre_addition,
                                res0_post_addition,
                                res0_around_addition,
                                res0_whole_addition]

        new_result_list = [res1_pre_change,       # correctly filtered out
                           res1_change,           # correctly kept
                           res1_post_change,      # correctly filtered out
                           res1_around_change,    # correctly filtered out
                           res1_with_change,      # correctly kept
                           res1_whole_change,     # correctly kept

                           res1_pre_remove,       # correctly filtered out
                           res1_post_remove,      # FALSE POSITIVE (in-line)
                           res1_around_remove,    # correctly filtered out
                           res1_whole_remove,     # correctly kept

                           res1_pre_addition,     # correctly filtered out
                           res1_addition,         # correctly kept
                           res1_post_addition,    # correctly filtered out
                           res1_around_addition,  # FALSE POSITIVE (close-line)
                           res1_with_addition,    # correctly kept
                           res1_whole_addition]   # correctly kept

        unique_new_result_list = [res1_change,           # correct
                                  res1_with_change,      # correct
                                  res1_whole_change,     # correct

                                  res1_addition,         # correct
                                  res1_around_addition,  # WRONG: line-wise diff
                                  res1_with_addition,    # correct
                                  res1_whole_addition]   # correct

        with open(self.original_file_name, 'r') as original_file:
            original_file_dict = {
                abspath('file_name'): original_file.readlines()}

            with open(self.modified_file_name, 'r') as modified_file:
                modified_file_dict = {
                    abspath('file_name'): modified_file.readlines()}

                # 'TIS THE IMPORTANT PART
                self.assertEqual(sorted(filter_results(original_file_dict,
                                                       modified_file_dict,
                                                       original_result_list,
                                                       new_result_list)),
                                 sorted(unique_new_result_list))

    def test_affected_code_rename_files(self):

        # ORIGINAL SOURCE RANGES:
        sr0_pre_change = SourceRange.from_values('file_name',
                                                 start_line=8,
                                                 start_column=1,
                                                 end_line=8,
                                                 end_column=3)

        # ORIGINAL RESULTS:
        res0_pre_change = Result(origin='origin',
                                 message='message',
                                 affected_code=(sr0_pre_change,))

        # NEW SOURCE RANGES:
        sr1_pre_change = SourceRange.from_values('file_name_new',
                                                 start_line=7,
                                                 start_column=1,
                                                 end_line=7,
                                                 end_column=3)
        sr1_change = SourceRange.from_values('file_name_new',
                                             start_line=4,
                                             start_column=8,
                                             end_line=4,
                                             end_column=13)

        # NEW RESULTS:
        res1_pre_change = Result(origin='origin',
                                 message='message',
                                 affected_code=(sr1_pre_change,))
        res1_change = Result(origin='origin',
                             message='message',
                             affected_code=(sr1_change,))
        res1_whole_remove = Result.from_values(origin='origin',
                                               message='message',
                                               file='file_name_new',
                                               line=6,
                                               column=1,
                                               end_line=7,
                                               end_column=5)

        original_result_list = [res0_pre_change]

        new_result_list = [res1_pre_change,
                           res1_change,
                           res1_whole_remove]

        unique_new_result_list = [res1_change,
                                  res1_whole_remove]

        with open(self.original_file_name, 'r') as original_file:
            original_file_dict = {
                abspath('file_name'): original_file.readlines()}

            with open(self.modified_file_name, 'r') as modified_file:
                modified_file_dict = {
                    abspath('file_name_new'): modified_file.readlines()}

                # 'TIS THE IMPORTANT PART
                self.assertEqual(sorted(filter_results(original_file_dict,
                                                       modified_file_dict,
                                                       original_result_list,
                                                       new_result_list)),
                                 sorted(unique_new_result_list))

    def test_unrelated_file_change(self):
        testfile_1 = ['1\n', '2\n']
        testfile_2 = ['1\n', '2\n']
        testfile_2_new = ['0\n', '1\n', '2\n']
        old_result = Result.from_values('origin', 'message', 'tf1', 1)
        new_result = Result.from_values('origin', 'message', 'tf1', 1)
        tf1 = abspath('tf1')
        original_file_dict = {tf1: testfile_1, 'tf2': testfile_2}
        modified_file_dict = {tf1: testfile_1, 'tf2': testfile_2_new}

        new_results = filter_results(original_file_dict, modified_file_dict,
                                     [old_result], [new_result])
        self.assertEqual(new_results, [])

    def test_result_range(self):
        test_file = ['123456789', '123456789', '123456789', '123456789']

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values('file',
                                                              1,
                                                              1,
                                                              1,
                                                              1)),
                         ['23456789', '123456789', '123456789', '123456789'])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values('file',
                                                              1,
                                                              9,
                                                              1,
                                                              9)),
                         ['12345678', '123456789', '123456789', '123456789'])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values('file',
                                                              1,
                                                              3,
                                                              1,
                                                              7)),
                         ['1289', '123456789', '123456789', '123456789'])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values('file',
                                                              1,
                                                              3,
                                                              2,
                                                              7)),
                         ['12', '89', '123456789', '123456789'])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values('file',
                                                              1,
                                                              3,
                                                              3,
                                                              7)),
                         ['12', '89', '123456789'])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values('file',
                                                              1,
                                                              3,
                                                              4,
                                                              7)),
                         ['12', '89'])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values('file',
                                                              None,
                                                              None,
                                                              None,
                                                              None)),
                         [])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values('file',
                                                              None,
                                                              None,
                                                              3,
                                                              None)),
                         ['123456789'])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values('file',
                                                              3,
                                                              None,
                                                              3,
                                                              None)),
                         ['123456789', '123456789', '123456789'])

    def test_result_range_inline_overlap(self):
        test_file = ['123456789\n']
        test_file_dict = {abspath('test_file'): test_file}

        source_range1 = SourceRange.from_values('test_file', 1, 1, 1, 4)
        source_range2 = SourceRange.from_values('test_file', 1, 2, 1, 3)
        source_range3 = SourceRange.from_values('test_file', 1, 3, 1, 6)

        test_result = Result('origin',
                             'message',
                             (source_range1, source_range2, source_range3))

        result_diff = remove_result_ranges_diffs(
            [test_result],
            test_file_dict)[test_result][abspath('test_file')]
        expected_diff = Diff.from_string_arrays(test_file, ['789\n'])

        self.assertEqual(result_diff, expected_diff)

    def test_result_range_line_wise_overlap(self):
        test_file = ['11', '22', '33', '44', '55', '66']
        test_file_dict = {abspath('test_file'): test_file}

        source_range1 = SourceRange.from_values('test_file', 2, 2, 5, 1)
        source_range2 = SourceRange.from_values('test_file', 3, 1, 4, 1)

        test_result = Result('origin',
                             'message',
                             (source_range1, source_range2))

        result_diff = remove_result_ranges_diffs(
            [test_result],
            test_file_dict)[test_result][abspath('test_file')]
        expected_diff = Diff.from_string_arrays(test_file,
                                                ['11', '2', '5', '66'])

        self.assertEqual(result_diff, expected_diff)

    def test_no_range(self):
        test_file = ['abc']
        test_file_dict = {abspath('test_file'): test_file}

        test_result = Result('origin',
                             'message')

        result_diff = remove_result_ranges_diffs(
            [test_result],
            test_file_dict)[test_result][abspath('test_file')]
        expected_diff = Diff.from_string_arrays(test_file, ['abc'])

        self.assertEqual(result_diff, expected_diff)

    def test_new_file_with_result(self):
        testfile_1 = ['1\n', '2\n']
        testfile_2_new = ['0\n', '1\n', '2\n']
        tf1 = abspath('tf1')
        tf2 = abspath('tf2')
        old_result = Result.from_values('origin', 'message', 'tf1', 1)
        new_result = Result.from_values('origin', 'message', 'tf2', 1)
        original_file_dict = {tf1: testfile_1}
        modified_file_dict = {tf1: testfile_1, tf2: testfile_2_new}

        new_results = filter_results(original_file_dict, modified_file_dict,
                                     [old_result], [new_result])
        self.assertEqual(new_results, [new_result])

    def test_delete_file_with_result(self):
        testfile_1 = ['1\n', '2\n']
        testfile_2 = ['0\n', '1\n', '2\n']
        testfile_1_new = ['0\n', '1\n', '2\n']
        tf1 = abspath('tf1')
        tf2 = abspath('tf2')
        old_result_tf1 = Result.from_values('origin', 'message', 'tf1', 1)
        old_result_tf2 = Result.from_values('origin', 'message', 'tf2', 1)
        new_result = Result.from_values('origin', 'message', 'tf1', 1)
        original_file_dict = {tf1: testfile_1, tf2: testfile_2}
        modified_file_dict = {tf1: testfile_1_new}

        new_results = filter_results(original_file_dict,
                                     modified_file_dict,
                                     [old_result_tf1, old_result_tf2],
                                     [new_result])
        self.assertEqual(new_results, [new_result])
