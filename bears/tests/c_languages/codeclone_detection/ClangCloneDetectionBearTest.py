import os
import unittest
from queue import Queue

from bears.tests.BearTestHelper import generate_skip_decorator
from bears.c_languages.codeclone_detection.ClangFunctionDifferenceBear import (
    ClangFunctionDifferenceBear)
from bears.c_languages.codeclone_detection.ClangCloneDetectionBear import (
    ClangCloneDetectionBear)
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@generate_skip_decorator(ClangCloneDetectionBear)
class ClangCloneDetectionBearTest(unittest.TestCase):

    def setUp(self):
        self.base_test_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "clone_detection_samples"))
        self.section = Section("default")
        self.section.append(Setting("files", "", origin=self.base_test_path))
        self.section.append(Setting("max_clone_difference", "0.308"))
        self.clone_files = [os.listdir(os.path.join(self.base_test_path,
                                                    "clones"))]

    def test_dependencies(self):
        self.assertIn(ClangFunctionDifferenceBear,
                      ClangCloneDetectionBear.get_dependencies())

    def test_configuration(self):
        self.section.append(Setting("average_calculation", "true"))
        self.section.append(Setting("poly_postprocessing", "false"))
        self.section.append(Setting("exp_postprocessing", "true"))

        self.clone_files = [
            os.path.join(self.base_test_path, "clones", "s4c.c")]

        # Ignore the results, it may be possible that it still passes :)
        self.check_clone_detection_bear(self.clone_files,
                                        lambda results, msg: True)

    def test_non_clones(self):
        self.non_clone_files = [
            os.path.join(self.base_test_path, "non_clones", elem)
            for elem in os.listdir(os.path.join(self.base_test_path,
                                                "non_clones"))]

        self.check_clone_detection_bear(self.non_clone_files,
                                        lambda results, msg:
                                        self.assertEqual(results, [], msg))

    def test_clones(self):
        self.clone_files = [
            os.path.join(self.base_test_path, "clones", elem)
            for elem in os.listdir(os.path.join(self.base_test_path,
                                                "clones"))]

        self.check_clone_detection_bear(self.clone_files,
                                        lambda results, msg:
                                        self.assertNotEqual(results, [], msg))

    def check_clone_detection_bear(self, files, result_check_function):
        """
        Checks the results of the CloneDetectionBear with the given function.

        :param files:                 The files to check. Each will be checked
                                      on its own.
        :param result_check_function: A function yielding an exception if the
                                      results are invalid.
        """
        for file in files:
            difference_results = ClangFunctionDifferenceBear(
                {file: ""},
                self.section,
                Queue()).run_bear_from_section([], {})
            uut = ClangCloneDetectionBear(
                {file: ""},
                self.section,
                Queue())
            arg_dict = {"dependency_results":
                        {ClangFunctionDifferenceBear.__name__:
                         list(difference_results)}}

            result_check_function(
                list(uut.run_bear_from_section([], arg_dict)),
                "while analyzing "+file)


if __name__ == '__main__':
    unittest.main(verbosity=2)
