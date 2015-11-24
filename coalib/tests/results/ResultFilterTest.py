import os
import sys
import unittest

sys.path.insert(0, ".")
from coalib.results.ResultFilter import filter_results
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
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

        # ORIGINAL SOURCE RANGES:
        sr0_pre_change = SourceRange.from_values("file_name",
                                                 start_line=4,
                                                 start_column=1,
                                                 end_line=4,
                                                 end_column=6)
        sr0_change = SourceRange.from_values("file_name",
                                             start_line=4,
                                             start_column=8,
                                             end_line=4,
                                             end_column=13)
        sr0_post_change = SourceRange.from_values("file_name",
                                                  start_line=4,
                                                  start_column=15,
                                                  end_line=4,
                                                  end_column=19)

        sr0_pre_remove = SourceRange.from_values("file_name",
                                                 start_line=6,
                                                 start_column=1,
                                                 end_line=6,
                                                 end_column=6)
        sr0_post_remove = SourceRange.from_values("file_name",
                                                  start_line=8,
                                                  start_column=1,
                                                  end_line=8,
                                                  end_column=5)

        sr0_pre_addition = SourceRange.from_values("file_name",
                                                   start_line=10,
                                                   start_column=1,
                                                   end_line=10,
                                                   end_column=6)
        sr0_post_addition = SourceRange.from_values("file_name",
                                                    start_line=11,
                                                    start_column=1,
                                                    end_line=11,
                                                    end_column=5)

        # ORIGINAL RESULTS:
        res0_pre_change = Result(origin="origin",
                                 message="message",
                                 affected_code=(sr0_pre_change,))
        res0_change = Result(origin="origin",
                             message="message",
                             affected_code=(sr0_change,))
        res0_post_change = Result(origin="origin",
                                  message="message",
                                  affected_code=(sr0_post_change,))
        res0_around_change = Result(origin="origin",
                                    message="message",
                                    affected_code=(sr0_pre_change,
                                                   sr0_post_change))
        res0_with_change = Result(origin="origin",
                                  message="message",
                                  affected_code=(sr0_pre_change,
                                                 sr0_change,
                                                 sr0_post_change))
        res0_whole_change = Result.from_values(origin="origin",
                                               message="message",
                                               file="file_name",
                                               line=4,
                                               column=1,
                                               end_line=4,
                                               end_column=19)

        res0_pre_remove = Result(origin="origin",
                                 message="message",
                                 affected_code=(sr0_pre_remove,))
        res0_post_remove = Result(origin="origin",
                                  message="message",
                                  affected_code=(sr0_post_remove,))
        res0_around_remove = Result(origin="origin",
                                    message="message",
                                    affected_code=(sr0_pre_remove,
                                                   sr0_post_remove))
        res0_whole_remove = Result.from_values(origin="origin",
                                               message="message",
                                               file="file_name",
                                               line=6,
                                               column=1,
                                               end_line=8,
                                               end_column=5)

        res0_pre_addition = Result(origin="origin",
                                   message="message",
                                   affected_code=(sr0_pre_addition,))
        res0_post_addition = Result(origin="origin",
                                    message="message",
                                    affected_code=(sr0_post_addition,))
        res0_around_addition = Result(origin="origin",
                                      message="message",
                                      affected_code=(sr0_pre_addition,
                                                     sr0_post_addition))
        res0_whole_addition = Result.from_values(origin="origin",
                                                 message="message",
                                                 file="file_name",
                                                 line=10,
                                                 column=1,
                                                 end_line=11,
                                                 end_column=5)

        # NEW SOURCE RANGES:
        sr1_pre_change = SourceRange.from_values("file_name",
                                                 start_line=4,
                                                 start_column=1,
                                                 end_line=4,
                                                 end_column=6)
        sr1_change = SourceRange.from_values("file_name",
                                             start_line=4,
                                             start_column=8,
                                             end_line=4,
                                             end_column=13)
        sr1_post_change = SourceRange.from_values("file_name",
                                                  start_line=4,
                                                  start_column=15,
                                                  end_line=4,
                                                  end_column=19)

        sr1_pre_remove = SourceRange.from_values("file_name",
                                                 start_line=6,
                                                 start_column=1,
                                                 end_line=6,
                                                 end_column=6)
        sr1_post_remove = SourceRange.from_values("file_name",
                                                  start_line=7,
                                                  start_column=1,
                                                  end_line=7,
                                                  end_column=5)

        sr1_pre_addition = SourceRange.from_values("file_name",
                                                   start_line=9,
                                                   start_column=1,
                                                   end_line=9,
                                                   end_column=6)
        sr1_addition = SourceRange.from_values("file_name",
                                               start_line=10,
                                               start_column=1,
                                               end_line=10,
                                               end_column=8)
        sr1_post_addition = SourceRange.from_values("file_name",
                                                    start_line=11,
                                                    start_column=1,
                                                    end_line=11,
                                                    end_column=5)

        # NEW RESULTS:
        res1_pre_change = Result(origin="origin",
                                 message="message",
                                 affected_code=(sr1_pre_change,))
        res1_change = Result(origin="origin",
                             message="message",
                             affected_code=(sr1_change,))
        res1_post_change = Result(origin="origin",
                                  message="message",
                                  affected_code=(sr1_post_change,))
        res1_around_change = Result(origin="origin",
                                    message="message",
                                    affected_code=(sr1_pre_change,
                                                   sr1_post_change))
        res1_with_change = Result(origin="origin",
                                  message="message",
                                  affected_code=(sr1_pre_change,
                                                 sr1_change,
                                                 sr1_post_change))
        res1_whole_change = Result.from_values(origin="origin",
                                               message="message",
                                               file="file_name",
                                               line=4,
                                               column=1,
                                               end_line=4,
                                               end_column=19)

        res1_pre_remove = Result(origin="origin",
                                 message="message",
                                 affected_code=(sr1_pre_remove,))
        res1_post_remove = Result(origin="origin",
                                  message="message",
                                  affected_code=(sr1_post_remove,))
        res1_around_remove = Result(origin="origin",
                                    message="message",
                                    affected_code=(sr1_pre_remove,
                                                   sr1_post_remove))
        res1_whole_remove = Result.from_values(origin="origin",
                                               message="message",
                                               file="file_name",
                                               line=6,
                                               column=1,
                                               end_line=7,
                                               end_column=5)

        res1_pre_addition = Result(origin="origin",
                                   message="message",
                                   affected_code=(sr1_pre_addition,))
        res1_addition = Result(origin="origin",
                               message="message",
                               affected_code=(sr1_addition,))
        res1_post_addition = Result(origin="origin",
                                    message="message",
                                    affected_code=(sr1_post_addition,))
        res1_around_addition = Result(origin="origin",
                                      message="message",
                                      affected_code=(sr1_pre_addition,
                                                     sr1_post_addition))
        res1_with_addition = Result(origin="origin",
                                    message="message",
                                    affected_code=(sr1_pre_addition,
                                                   sr1_addition,
                                                   sr1_post_addition))
        res1_whole_addition = Result.from_values(origin="origin",
                                                 message="message",
                                                 file="file_name",
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

        new_result_list = [res1_pre_change,#
                           res1_change,#
                           res1_post_change,#
                           res1_around_change,#
                           res1_with_change,#
                           res1_whole_change,#

                           res1_pre_remove,
                           res1_post_remove,#
                           res1_around_remove,
                           res1_whole_remove,

                           res1_pre_addition,
                           res1_addition,#
                           res1_post_addition,
                           res1_around_addition,
                           res1_with_addition,
                           res1_whole_addition]

        unique_new_result_list = [res1_change,# check, pre_change
                                  res1_with_change,
                                  res1_whole_change,

                                  res1_whole_remove,

                                  res1_addition,
                                  res1_with_addition,
                                  res1_whole_addition]

        with open(self.original_file_name, "r") as original_file:
            original_file_dict = {
                "file_name": original_file.readlines()}

            with open(self.modified_file_name, "r") as modified_file:
                modified_file_dict = {
                    "file_name": modified_file.readlines()}

                # print(list(filter_results(original_file_dict,
                #                                        modified_file_dict,
                #                                        original_result_list,
                #                                        new_result_list))[0],
                #       "\n\n")
                #
                # print(list(filter_results(original_file_dict,
                #                                        modified_file_dict,
                #                                        original_result_list,
                #                                        new_result_list))[1],
                #       "\n\n")
                #
                # print(list(filter_results(original_file_dict,
                #                                        modified_file_dict,
                #                                        original_result_list,
                #                                        new_result_list))[2],
                #       "\n\n")
                #
                # print(list(filter_results(original_file_dict,
                #                                        modified_file_dict,
                #                                        original_result_list,
                #                                        new_result_list))[3],
                #       "\n\n")
                #
                # print(list(filter_results(original_file_dict,
                #                                        modified_file_dict,
                #                                        original_result_list,
                #                                        new_result_list))[4],
                #       "\n\n")
                #
                # print(list(filter_results(original_file_dict,
                #                                        modified_file_dict,
                #                                        original_result_list,
                #                                        new_result_list))[5],
                #       "\n\n")
                #
                # print(list(filter_results(original_file_dict,
                #                                        modified_file_dict,
                #                                        original_result_list,
                #                                        new_result_list))[6],
                #       "\n\n")
                #
                # print(list(filter_results(original_file_dict,
                #                                        modified_file_dict,
                #                                        original_result_list,
                #                                        new_result_list))[7],
                #       "\n\n")

                # 'TIS THE IMPORTANT PART
                self.assertEqual(sorted(filter_results(original_file_dict,
                                                       modified_file_dict,
                                                       original_result_list,
                                                       new_result_list)),
                                 sorted(unique_new_result_list))

    def test_diffs(self):
        self.assertTrue(True)
        # TODO


if __name__ == '__main__':
    unittest.main(verbosity=2)
