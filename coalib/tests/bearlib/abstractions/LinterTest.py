import os
import sys
import unittest

from coalib.bearlib.abstractions.Linter import Linter
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.FunctionMetadata import FunctionMetadata
from coalib.settings.Section import Section


def get_testfile_name(name):
    """
    Gets the full path to a testfile inside ``linter_test_files`` directory.

    :param name: The filename of the testfile to get the full path for.
    :return:     The full path to given testfile name.
    """
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        "linter_test_files",
                        name)


class LinterComponentTest(unittest.TestCase):

    class EmptyTestLinter:
        pass

    def setUp(self):
        self.section = Section("TEST_SECTION")

    def test_decorator_invalid_parameters(self):
        with self.assertRaises(ValueError) as cm:
            Linter("some-executable", output_regex="", invalid_arg=88)
        self.assertEqual(str(cm.exception),
                         "Invalid keyword argument 'invalid_arg' provided.")

        with self.assertRaises(ValueError) as cm:
            Linter("some-executable",
                   output_regex="",
                   diff_severity=RESULT_SEVERITY.MAJOR)
        self.assertEqual(str(cm.exception),
                         "Invalid keyword argument 'diff_severity' provided.")

        with self.assertRaises(ValueError) as cm:
            Linter("some-executable",
                   output_regex="",
                   diff_message="Custom message")
        self.assertEqual(str(cm.exception),
                         "Invalid keyword argument 'diff_message' provided.")

        with self.assertRaises(ValueError) as cm:
            Linter("some-executable",
                   provides_correction=True,
                   output_regex=".*")
        self.assertEqual(str(cm.exception),
                         "Invalid keyword argument 'output_regex' provided.")

        with self.assertRaises(ValueError) as cm:
            Linter("some-executable",
                   provides_correction=True,
                   severity_map={})
        self.assertEqual(str(cm.exception),
                         "Invalid keyword argument 'severity_map' provided.")

    def test_decorator_invalid_states(self):
        with self.assertRaises(ValueError) as cm:
            Linter("some-executable")
        self.assertEqual(str(cm.exception), "No `output_regex` specified.")

        with self.assertRaises(ValueError) as cm:
            Linter("some-executable", output_regex="", severity_map={})
        self.assertEqual(
            str(cm.exception),
            "Provided `severity_map` but named group `severity` is not used "
            "in `output_regex`.")

    def test_decorator_invalid_parameter_types(self):
        with self.assertRaises(TypeError):
            Linter("some-executable",
                   output_regex="(?P<severity>)",
                   severity_map=list())

        with self.assertRaises(TypeError):
            Linter("some-executable",
                   provides_correction=True,
                   diff_message=list())

        with self.assertRaises(TypeError) as cm:
            Linter("some-executable",
                   provides_correction=True,
                   diff_severity=999888777)
        self.assertEqual(str(cm.exception),
                         "Invalid value for `diff_severity`: 999888777")

    def test_get_executable(self):
        uut = Linter("some-executable", output_regex="")(self.EmptyTestLinter)
        self.assertEqual(uut.get_executable(), "some-executable")

    def test_check_prerequisites(self):
        uut = Linter(sys.executable, output_regex="")(self.EmptyTestLinter)
        self.assertTrue(uut.check_prerequisites())

        uut = (Linter("invalid_nonexisting_programv412", output_regex="")
               (self.EmptyTestLinter))
        self.assertEqual(uut.check_prerequisites(),
                         "'invalid_nonexisting_programv412' is not installed.")

    def test_execute_command(self):
        test_program_path = get_testfile_name("stdout_stderr.py")
        uut = Linter(sys.executable, output_regex="")(self.EmptyTestLinter)

        # The test program puts out the stdin content (only the first line) to
        # stdout and the arguments passed to stderr.
        stdout, stderr = uut._execute_command(
            [test_program_path, "some_argument"],
            stdin="display content")

        self.assertEqual(stdout, "display content\n")
        self.assertEqual(stderr, "['some_argument']\n")

    def test_process_output_corrected(self):
        uut = (Linter(sys.executable, provides_correction=True)
               (self.EmptyTestLinter)
               (self.section, None))

        original = [s + "\n" for s in ["void main()  {", "return 09;", "}"]]
        fixed = [s + "\n" for s in ["void main()", "{", "return 9;", "}"]]

        results = list(uut._process_output("".join(fixed),
                                           "some-file.c",
                                           original))

        diffs = list(Diff.from_string_arrays(original, fixed).split_diff())
        expected = [Result.from_values(uut,
                                       "Inconsistency found.",
                                       "some-file.c",
                                       1,
                                       None,
                                       2,
                                       None,
                                       RESULT_SEVERITY.NORMAL,
                                       diffs={"some-file.c": diffs[0]})]

        self.assertEqual(results, expected)

    def test_process_output_issues(self):
        test_output = ("12:4-14:0-Serious issue (error) -> ORIGIN=X\n"
                       "0:0-0:1-This is a warning (warning) -> ORIGIN=Y\n"
                       "813:77-1024:32-Just a note (info) -> ORIGIN=Z\n")
        regex = (r"(?P<line>\d+):(?P<column>\d+)-"
                 r"(?P<end_line>\d+):(?P<end_column>\d+)-"
                 r"(?P<message>.*) \((?P<severity>.*)\) -> "
                 r"ORIGIN=(?P<origin>.*)")

        uut = (Linter(sys.executable, output_regex=regex)
               (self.EmptyTestLinter)
               (self.section, None))
        sample_file = "some-file.xtx"
        results = list(uut._process_output(test_output, sample_file, [""]))
        expected = [Result.from_values("EmptyTestLinter (X)",
                                       "Serious issue",
                                       sample_file,
                                       12,
                                       4,
                                       14,
                                       0,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values("EmptyTestLinter (Y)",
                                       "This is a warning",
                                       sample_file,
                                       0,
                                       0,
                                       0,
                                       1,
                                       RESULT_SEVERITY.NORMAL),
                    Result.from_values("EmptyTestLinter (Z)",
                                       "Just a note",
                                       sample_file,
                                       813,
                                       77,
                                       1024,
                                       32,
                                       RESULT_SEVERITY.INFO)]

        self.assertEqual(results, expected)

    def test_get_non_optional_settings(self):
        class Handler:

            @staticmethod
            def create_arguments(filename, file, config_file, param_x: int):
                pass

            @staticmethod
            def generate_config(filename, file, superparam):
                """
                :param superparam: A superparam!
                """
                return None

        uut = Linter(sys.executable, output_regex="")(Handler)

        self.assertEqual(uut.get_non_optional_settings(),
                         {"param_x": ("No description given.", int),
                          "superparam": ("A superparam!", None)})

    def test_section_settings_forwarding(self):
        class Handler:

            @staticmethod
            def create_arguments(filename, file, config_file, my_param: int):
                self.assertEqual(filename, "some_file.cs")
                self.assertEqual(file, [])
                self.assertIsNone(config_file)
                self.assertEqual(my_param, 109)
                # Execute python and do nothing.
                return "-c", "pass"

            @staticmethod
            def generate_config(filename, file, my_config_param: int):
                self.assertEqual(filename, "some_file.cs")
                self.assertEqual(file, [])
                self.assertEqual(my_config_param, 88)
                return None

        self.section["my_param"] = "109"
        self.section["my_config_param"] = "88"

        uut = (Linter(sys.executable, output_regex="")
               (Handler)
               (self.section, None))

        self.assertIsNotNone(list(uut.execute(filename="some_file.cs",
                                              file=[])))

    def test_grab_output(self):
        uut = (Linter("", use_stderr=False, output_regex="")
               (self.EmptyTestLinter))
        self.assertEqual(uut._grab_output("std", "err"), "std")

        uut = (Linter("", use_stderr=True, output_regex="")
               (self.EmptyTestLinter))
        self.assertEqual(uut._grab_output("std", "err"), "err")

    def test_pass_file_as_stdin_if_needed(self):
        uut = (Linter("", use_stdin=False, output_regex="")
               (self.EmptyTestLinter))
        self.assertIsNone(uut._pass_file_as_stdin_if_needed(["contents"]))

        uut = Linter("", use_stdin=True, output_regex="")(self.EmptyTestLinter)
        self.assertEqual(uut._pass_file_as_stdin_if_needed(
                             ["contents\n", "X"]),
                         "contents\nX")

    def test_generate_config(self):
        uut = Linter("", output_regex="")(self.EmptyTestLinter)
        with uut._create_config("filename", []) as config_file:
            self.assertIsNone(config_file)

        class ConfigurationTestLinter:

            @staticmethod
            def generate_config(filename, file, val):
                return "config_value = " + str(val)

        uut = (Linter("", output_regex="", config_suffix=".xml")
               (ConfigurationTestLinter))
        with uut._create_config("filename", [], val=88) as config_file:
            self.assertTrue(os.path.isfile(config_file))
            self.assertEqual(config_file[-4:], ".xml")
            with open(config_file, mode="r") as fl:
                self.assertEqual(fl.read(), "config_value = 88")
        self.assertFalse(os.path.isfile(config_file))

    def test_merge_metadata(self):
        uut = Linter("", output_regex="")(self.EmptyTestLinter)

        metadata1 = FunctionMetadata(
            "main",
            "Desc of main.\n",
            "Returns 0 on success",
            {"argc": ("argc desc", None), "argv": ("argv desc", None)},
            {"opt": ("opt desc", int, 88)},
            {"self", "A"})

        metadata2 = FunctionMetadata(
            "process",
            "Desc of process.\n",
            "Returns the processed stuff.",
            {"argc": ("argc desc from process", int),
             "to_process": ("to_process desc", int)},
            {"opt2": ("opt2 desc", str, "hello")},
            {"self", "B"})

        merged_metadata = uut._merge_metadata(metadata1, metadata2)

        self.assertEqual(
            merged_metadata.name,
            "<Merged signature of 'main' and 'process'>")
        self.assertEqual(
            merged_metadata.desc,
            "main:\nDesc of main.\n\nprocess:\nDesc of process.\n")
        self.assertEqual(
            merged_metadata.retval_desc,
            "main:\nReturns 0 on success\nprocess:\nReturns the processed "
            "stuff.")
        self.assertEqual(
            merged_metadata.non_optional_params,
            {"argc": ("argc desc from process", int),
             "argv": ("argv desc", None),
             "to_process": ("to_process desc", int)})
        self.assertEqual(
            merged_metadata.optional_params,
            {"opt": ("opt desc", int, 88),
             "opt2": ("opt2 desc", str, "hello")})
        self.assertEqual(
            merged_metadata.omit,
            frozenset({"self", "A", "B"}))


class LinterReallifeTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("REALLIFE_TEST_SECTION")

        self.test_program_path = get_testfile_name("test_linter.py")
        self.test_program_regex = (
            r"L(?P<line>\d+)C(?P<column>\d+)-"
            r"L(?P<end_line>\d+)C(?P<end_column>\d+):"
            r" (?P<message>.*) \| (?P<severity>.+) SEVERITY")
        self.test_program_severity_map = {"MAJOR": RESULT_SEVERITY.MAJOR}

        self.testfile_path = get_testfile_name("test_file.txt")
        with open(self.testfile_path, mode="r") as fl:
            self.testfile_content = fl.read().splitlines(keepends=True)

        self.testfile2_path = get_testfile_name("test_file2.txt")
        with open(self.testfile2_path, mode="r") as fl:
            self.testfile2_content = fl.read().splitlines(keepends=True)

    def test_nostdin_nostderr_noconfig_nocorrection(self):
        class Handler:

            @staticmethod
            def create_arguments(filename, file, config_file):
                self.assertEqual(filename, self.testfile_path)
                self.assertEqual(file, self.testfile_content)
                self.assertIsNone(config_file)
                return self.test_program_path, filename

        uut = (Linter(sys.executable,
                      output_regex=self.test_program_regex,
                      severity_map=self.test_program_severity_map)
               (Handler)
               (self.section, None))

        results = list(uut.run(self.testfile_path, self.testfile_content))
        expected = [Result.from_values(uut,
                                       "Invalid char ('0')",
                                       self.testfile_path,
                                       3,
                                       0,
                                       3,
                                       1,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values(uut,
                                       "Invalid char ('.')",
                                       self.testfile_path,
                                       5,
                                       0,
                                       5,
                                       1,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values(uut,
                                       "Invalid char ('p')",
                                       self.testfile_path,
                                       9,
                                       0,
                                       9,
                                       1,
                                       RESULT_SEVERITY.MAJOR)]

        self.assertEqual(results, expected)

    def test_stdin_stderr_noconfig_nocorrection(self):
        class Handler:

            @staticmethod
            def create_arguments(filename, file, config_file):
                self.assertEqual(filename, self.testfile2_path)
                self.assertEqual(file, self.testfile2_content)
                self.assertIsNone(config_file)
                return (self.test_program_path,
                        "--use_stderr",
                        "--use_stdin",
                        filename)

        uut = (Linter(sys.executable,
                      use_stdin=True,
                      use_stderr=True,
                      output_regex=self.test_program_regex,
                      severity_map=self.test_program_severity_map)
               (Handler)
               (self.section, None))

        results = list(uut.run(self.testfile2_path, self.testfile2_content))
        expected = [Result.from_values(uut,
                                       "Invalid char ('X')",
                                       self.testfile2_path,
                                       0,
                                       0,
                                       0,
                                       1,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values(uut,
                                       "Invalid char ('i')",
                                       self.testfile2_path,
                                       4,
                                       0,
                                       4,
                                       1,
                                       RESULT_SEVERITY.MAJOR)]

        self.assertEqual(results, expected)

    def test_nostdin_nostderr_noconfig_correction(self):
        class Handler:

            @staticmethod
            def create_arguments(filename, file, config_file):
                self.assertEqual(filename, self.testfile_path)
                self.assertEqual(file, self.testfile_content)
                self.assertIsNone(config_file)
                return self.test_program_path, "--correct", filename

        uut = (Linter(sys.executable,
                      provides_correction=True,
                      diff_severity=RESULT_SEVERITY.INFO,
                      diff_message="Custom message")
               (Handler)
               (self.section, None))

        results = list(uut.run(self.testfile_path, self.testfile_content))

        expected_correction = ["+", "-", "*", "++", "-", "-", "+"]
        expected_correction = [s + "\n" for s in expected_correction]

        diffs = list(Diff.from_string_arrays(
            self.testfile_content,
            expected_correction).split_diff())

        expected = [Result.from_values(uut,
                                       "Custom message",
                                       self.testfile_path,
                                       4,
                                       None,
                                       4,
                                       None,
                                       RESULT_SEVERITY.INFO,
                                       diffs={self.testfile_path: diffs[0]}),
                    Result.from_values(uut,
                                       "Custom message",
                                       self.testfile_path,
                                       6,
                                       None,
                                       6,
                                       None,
                                       RESULT_SEVERITY.INFO,
                                       diffs={self.testfile_path: diffs[1]}),
                    Result.from_values(uut,
                                       "Custom message",
                                       self.testfile_path,
                                       10,
                                       None,
                                       10,
                                       None,
                                       RESULT_SEVERITY.INFO,
                                       diffs={self.testfile_path: diffs[2]})]

        self.assertEqual(results, expected)

    def test_stdin_stderr_config_nocorrection(self):
        class Handler:

            @staticmethod
            def generate_config(filename, file, some_val):
                self.assertEqual(filename, self.testfile_path)
                self.assertEqual(file, self.testfile_content)
                # some_val shall only test the argument delegation from run().
                self.assertEqual(some_val, 33)

                return "\n".join(["use_stdin", "use_stderr"])

            @staticmethod
            def create_arguments(filename, file, config_file, some_val):
                self.assertEqual(filename, self.testfile_path)
                self.assertEqual(file, self.testfile_content)
                self.assertIsNotNone(config_file)
                self.assertEqual(some_val, 33)

                return self.test_program_path, "--config", config_file

        uut = (Linter(sys.executable,
                      use_stdin=True,
                      use_stderr=True,
                      output_regex=self.test_program_regex,
                      severity_map=self.test_program_severity_map)
               (Handler)
               (self.section, None))

        results = list(uut.run(self.testfile_path,
                               self.testfile_content,
                               some_val=33))
        expected = [Result.from_values(uut,
                                       "Invalid char ('0')",
                                       self.testfile_path,
                                       3,
                                       0,
                                       3,
                                       1,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values(uut,
                                       "Invalid char ('.')",
                                       self.testfile_path,
                                       5,
                                       0,
                                       5,
                                       1,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values(uut,
                                       "Invalid char ('p')",
                                       self.testfile_path,
                                       9,
                                       0,
                                       9,
                                       1,
                                       RESULT_SEVERITY.MAJOR)]

        self.assertEqual(results, expected)

    def test_stdin_stderr_config_correction(self):
        # `some_value_A` and `some_value_B` are used to test the different
        # delegation to `generate_config()` and `create_arguments()`
        # accordingly.
        class Handler:

            @staticmethod
            def generate_config(filename, file, some_value_A):
                self.assertEqual(filename, self.testfile2_path)
                self.assertEqual(file, self.testfile2_content)
                self.assertEqual(some_value_A, 124)

                return "\n".join(["use_stdin", "use_stderr", "correct"])

            @staticmethod
            def create_arguments(filename, file, config_file, some_value_B):
                self.assertEqual(filename, self.testfile2_path)
                self.assertEqual(file, self.testfile2_content)
                self.assertEqual(config_file[-5:], ".conf")
                self.assertEqual(some_value_B, -78)

                return self.test_program_path, "--config", config_file

        uut = (Linter(sys.executable,
                      provides_correction=True,
                      use_stdin=True,
                      use_stderr=True,
                      config_suffix=".conf")
               (Handler)
               (self.section, None))

        results = list(uut.run(self.testfile2_path,
                               self.testfile2_content,
                               some_value_A=124,
                               some_value_B=-78))

        expected_correction = ["+", "/", "/", "-"]
        expected_correction = [s + "\n" for s in expected_correction]

        diffs = list(Diff.from_string_arrays(
            self.testfile2_content,
            expected_correction).split_diff())

        expected = [Result.from_values(uut,
                                       "Inconsistency found.",
                                       self.testfile2_path,
                                       1,
                                       None,
                                       1,
                                       None,
                                       RESULT_SEVERITY.NORMAL,
                                       diffs={self.testfile2_path: diffs[0]}),
                    Result.from_values(uut,
                                       "Inconsistency found.",
                                       self.testfile2_path,
                                       5,
                                       None,
                                       5,
                                       None,
                                       RESULT_SEVERITY.NORMAL,
                                       diffs={self.testfile2_path: diffs[1]})]

        self.assertEqual(results, expected)
