import sys
import unittest
import os
import inspect
from queue import Queue

sys.path.insert(0, ".")

from bears.codeclone_detection.ClangCloneDetectionBear import \
    ClangCloneDetectionBear
from coalib.bearlib.parsing.clang.cindex import Index, LibclangError
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class ClangCloneDetectionBearTest(unittest.TestCase):
    def setUp(self):
        self.base_test_path = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(ClangCloneDetectionBearTest)),
            "clone_detection_samples"))
        self.section = Section("default")
        self.section.append(Setting("condition_list",
                                    "used: 0.5, "
                                    "returned, "
                                    "is_condition, "
                                    "in_condition, "
                                    "in_second_level_condition, "
                                    "in_third_level_condition, "
                                    "is_assignee, "
                                    "is_assigner, "
                                    "loop_content, "
                                    "second_level_loop_content, "
                                    "third_level_loop_content, "
                                    "is_param, "
                                    "in_sum: 0.7, "
                                    "in_product: 0.7, "
                                    "in_binary_operation: 0.7,"
                                    "member_accessed"))
        self.clone_files = [os.listdir(os.path.join(self.base_test_path,
                                                    "clones"))]

    def test_invalid_conditions(self):
        self.section.append(Setting("condition_list", "bullshit"))

        self.uut = ClangCloneDetectionBear({}, self.section, Queue())
        self.assertEqual(self.uut.run_bear_from_section([], {}), None)

    def test_non_clones(self):
        self.non_clone_files = [
            os.path.join(self.base_test_path, "non_clones", elem)
            for elem in os.listdir(os.path.join(self.base_test_path,
                                                "non_clones"))]

        for file in self.non_clone_files:
            self.uut = ClangCloneDetectionBear({file: ""},
                                               self.section,
                                               Queue())
            self.assertEqual(self.uut.run_bear_from_section([], {}), [])

    def test_clones(self):
        self.clone_files = [
            os.path.join(self.base_test_path, "clones", elem)
            for elem in os.listdir(os.path.join(self.base_test_path,
                                                "clones"))]

        for file in self.clone_files:
            self.uut = ClangCloneDetectionBear({file: ""},
                                               self.section,
                                               Queue())
            self.assertNotEqual(self.uut.run_bear_from_section([], {}), [])


def skip_test():
    try:
        Index.create()
        return False
    except LibclangError as error:
        return str(error)


if __name__ == '__main__':
    unittest.main(verbosity=2)
