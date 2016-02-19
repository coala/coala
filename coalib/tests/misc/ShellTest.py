import os
import sys
import unittest
import shlex

from coalib.misc.Shell import (
    prepare_string_argument,
    run_interactive_shell_command, run_shell_command)


class RunShellCommandTest(unittest.TestCase):

    @staticmethod
    def construct_testscript_command(scriptname):
        return " ".join(
            shlex.quote(s) for s in (
                sys.executable,
                os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "run_shell_command_testfiles",
                             scriptname)))

    def test_run_interactive_shell_command(self):
        command = RunShellCommandTest.construct_testscript_command(
            "test_interactive_program.py")

        with run_interactive_shell_command(command) as p:
            self.assertEqual(p.stdout.readline(), "test_program X\n")
            self.assertEqual(p.stdout.readline(), "Type in a number:\n")
            p.stdin.write("33\n")
            p.stdin.flush()
            self.assertEqual(p.stdout.readline(), "33\n")
            self.assertEqual(p.stdout.readline(), "Exiting program.\n")

    def test_run_interactive_shell_command_kwargs_delegation(self):
        with self.assertRaises(TypeError):
            with run_interactive_shell_command("some_command",
                                               weird_parameter=30):
                pass

        # Test one of the forbidden parameters.
        with self.assertRaises(TypeError):
            with run_interactive_shell_command("some_command", shell=False):
                pass

    def test_run_shell_command_without_stdin(self):
        command = RunShellCommandTest.construct_testscript_command(
            "test_program.py")

        stdout, stderr = run_shell_command(command)

        expected = ("test_program Z\n"
                    "non-interactive mode.\n"
                    "Exiting...\n")
        self.assertEqual(stdout, expected)
        self.assertEqual(stderr, "")

    def test_run_shell_command_with_stdin(self):
        command = RunShellCommandTest.construct_testscript_command(
            "test_input_program.py")

        stdout, stderr = run_shell_command(command, "1  4  10  22")

        self.assertEqual(stdout, "37\n")
        self.assertEqual(stderr, "")

        stdout, stderr = run_shell_command(command, "1 p 5")

        self.assertEqual(stdout, "")
        self.assertEqual(stderr, "INVALID INPUT\n")

    def test_run_shell_command_kwargs_delegation(self):
        with self.assertRaises(TypeError):
            run_shell_command("super-cool-command", weird_parameter2="abc")

        # Test one of the forbidden parameters.
        with self.assertRaises(TypeError):
            run_shell_command("super-cool-command", universal_newlines=False)


class PrepareStringArgumentTest(unittest.TestCase):

    def setUp(self):
        self.test_strings = ("normal_string",
                             "string with spaces",
                             'string with quotes"a',
                             "string with s-quotes'b",
                             "bsn \n A",
                             "unrecognized \\q escape")

    def test_prepare_string_argument_sh(self):
        expected_results = ('"normal_string"',
                            '"string with spaces"',
                            '"string with quotes\\"a"',
                            '"string with s-quotes\'b"',
                            '"bsn \n A"',
                            '"unrecognized \\q escape"')

        for string, result in zip(self.test_strings, expected_results):
            self.assertEqual(prepare_string_argument(string, "sh"),
                             result)

    def test_prepare_string_argument_unsupported(self):
        for string in self.test_strings:
            self.assertEqual(prepare_string_argument(string, "WeIrD_O/S"),
                             string)
