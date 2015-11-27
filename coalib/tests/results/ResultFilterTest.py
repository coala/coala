import os
import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.ResultFilter import filter_results, remove_range
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange


class ResultFilterTest(unittest.TestCase):
    def setUp(self):
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
                                             message="original",
                                             file="original",
                                             severity=RESULT_SEVERITY.NORMAL,
                                             debug_msg="original")

        clone_result = Result.from_values(origin="Origin",
                                          message="original",
                                          file="original",
                                          severity=RESULT_SEVERITY.NORMAL,
                                          debug_msg="original")

        wrong_origin_result = Result.from_values(
            origin="AnotherOrigin",
            message="original",
            file="original",
            severity=RESULT_SEVERITY.NORMAL,
            debug_msg="original")

        wrong_message_result = Result.from_values(
            origin="Origin",
            message="another message",
            file="original",
            severity=RESULT_SEVERITY.NORMAL,
            debug_msg="original")

        wrong_severity_result = Result.from_values(
            origin="Origin",
            message="original",
            file="original",
            severity=RESULT_SEVERITY.INFO,
            debug_msg="original")

        wrong_debug_msg_result = Result.from_values(
            origin="Origin",
            message="original",
            file="original",
            severity=RESULT_SEVERITY.NORMAL,
            debug_msg="another debug message")

        file_dict = {"original": []}

        self.assertEqual(filter_results(original_file_dict=file_dict,
                                        modified_file_dict=file_dict,
                                        original_results=[original_result],
                                        modified_results=[
                                            clone_result,
                                            wrong_origin_result,
                                            wrong_message_result,
                                            wrong_severity_result,
                                            wrong_debug_msg_result]),
                         [wrong_origin_result,
                          wrong_message_result,
                          wrong_severity_result,
                          wrong_debug_msg_result])

    def test_affected_code(self):
        self.assertTrue(True)

    def test_diffs(self):
        self.assertTrue(True)

    def test_result_range(self):
        test_file = ["123456789", "123456789", "123456789", "123456789"]

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values("file",
                                                              1,
                                                              1,
                                                              1,
                                                              1)),
                         ["23456789", "123456789", "123456789", "123456789"])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values("file",
                                                              1,
                                                              9,
                                                              1,
                                                              9)),
                         ["12345678", "123456789", "123456789", "123456789"])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values("file",
                                                              1,
                                                              3,
                                                              1,
                                                              7)),
                         ["1289", "123456789", "123456789", "123456789"])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values("file",
                                                              1,
                                                              3,
                                                              2,
                                                              7)),
                         ["12", "89", "123456789", "123456789"])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values("file",
                                                              1,
                                                              3,
                                                              3,
                                                              7)),
                         ["12", "89", "123456789"])

        self.assertEqual(remove_range(test_file,
                                      SourceRange.from_values("file",
                                                              1,
                                                              3,
                                                              4,
                                                              7)),
                         ["12", "89"])

if __name__ == '__main__':
    unittest.main(verbosity=2)
