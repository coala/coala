import sys
import unittest
import os
from queue import Queue

sys.path.insert(0, ".")

from bears.codeclone_detection.ClangSimilarityBear import ClangSimilarityBear
from bears.codeclone_detection.ClangCloneDetectionBear import \
    ClangCloneDetectionBear
from coalib.bearlib.parsing.clang.cindex import Index, LibclangError
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class ClangCloneDetectionBearTest(unittest.TestCase):
    def setUp(self):
        self.base_test_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "clone_detection_samples"))
        self.section = Section("default")
        self.section.append(Setting("files", "", origin=self.base_test_path))
        self.clone_files = [os.listdir(os.path.join(self.base_test_path,
                                                    "clones"))]

    def test_dependencies(self):
        self.assertIn(ClangSimilarityBear,
                      ClangCloneDetectionBear.get_dependencies())

    def test_invalid_conditions(self):
        self.section.append(Setting("condition_list", "bullshit"))

        self.uut = ClangSimilarityBear({}, self.section, Queue())
        self.assertEqual(self.uut.run_bear_from_section([], {}), None)

    def test_non_clones(self):
        self.non_clone_files = [
            os.path.join(self.base_test_path, "non_clones", elem)
            for elem in os.listdir(os.path.join(self.base_test_path,
                                                "non_clones"))]

        self.check_clone_detection_bear(self.non_clone_files,
                                        lambda results:
                                        self.assertEqual(results, []))

    def test_clones(self):
        self.clone_files = [
            os.path.join(self.base_test_path, "clones", elem)
            for elem in os.listdir(os.path.join(self.base_test_path,
                                                "clones"))]

        self.check_clone_detection_bear(self.clone_files,
                                        lambda results:
                                        self.assertNotEqual(results, []))

    def check_clone_detection_bear(self, files, result_check_function):
        """
        Checks the results of the CloneDetectionBear with the given function.

        :param files:                 The files to check. Each will be checked
                                      on its own.
        :param result_check_function: A function yielding an exception if the
                                      results are invalid.
        """
        for file in files:
            similarity_results = ClangSimilarityBear(
                {file: ""},
                self.section,
                Queue()).run_bear_from_section([], {})
            uut = ClangCloneDetectionBear(
                {file: ""},
                self.section,
                Queue())
            arg_dict = {"dependency_results":
                        {"ClangSimilarityBear": similarity_results}}

            result_check_function(uut.run_bear_from_section([], arg_dict))


def skip_test():
    try:
        Index.create()
        return False
    except LibclangError as error:
        return str(error)


if __name__ == '__main__':
    unittest.main(verbosity=2)
