import sys
import unittest

from coalib import coala
import os
import tempfile

from tests.TestUtilities import execute_coala


class ConverterTest(unittest.TestCase):
    toml_file = """[all]
bears = ["coalaBear", "InvalidLinkBear", "FilenameBear", "LineCountBear"]
files = ["**.h", "**.rst", "**.json", "**.c", "**.yml", "**.py"]
ignore = ["yamllint/**/__pycache__/**", "yamllint/**/__pycache__"]
max_lines_per_file = 100

[python]
bears = ["BanditBear", "PyUnusedCodeBear", "CPDBear", "PycodestyleBear"]
language = "all.python"
inherits = ["all"]

[c]
bears = ["CSecurityBear", "GNUIndentBear", "DocGrammarBear"]
files = ["**.c", "**.h"]
language = "all.c"
inherits = ["all"]
"""

    coafile = """[all]
bears = coalaBear, InvalidLinkBear, FilenameBear, LineCountBear
files = **.h, **.rst, **.json, **.c, **.yml, **.py
ignore = yamllint/**/__pycache__/**, yamllint/**/__pycache__
max_lines_per_file = 100

[all.python]
bears = BanditBear, PyUnusedCodeBear, CPDBear, PycodestyleBear
language = all.python

[all.c]
bears = CSecurityBear, GNUIndentBear, DocGrammarBear
files = **.c, **.h
language = all.c
"""

    def setUp(self):
        self.old_argv = sys.argv
        self.tempdir = tempfile.gettempdir()
        self.input_coafile = os.path.join(self.tempdir, 'coafile_input.coafile')
        self.input_toml = os.path.join(self.tempdir, 'toml_input.toml')

        with open(self.input_coafile, 'w') as f:
            f.write(self.coafile)

        with open(self.input_toml, 'w') as f:
            f.write(self.toml_file)

    def test_coafile_to_toml(self):
        output_toml = os.path.join(self.tempdir, 'toml_output.toml')

        execute_coala(
            coala.main, 'coala', '-cc', self.input_coafile,
            output_toml)

        with open(output_toml, 'r') as f:
            lines = f.readlines()
        os.remove(output_toml)

        self.assertEqual(''.join(lines), self.toml_file)

    def test_toml_coafile(self):
        output_coafile = os.path.join(self.tempdir, 'coafile_output.coafile')

        execute_coala(
            coala.main, 'coala', '-cc', self.input_toml,
            output_coafile)

        with open(output_coafile, 'r') as f:
            lines = f.readlines()
        os.remove(output_coafile)

        self.assertEqual(''.join(lines), self.coafile)

    def test_unsupported_formats_error(self):

        with self.assertRaises(SystemExit):
            execute_coala(
                coala.main, 'coala', '-cc', '.coafile',
                '.coafile')

        with self.assertRaises(SystemExit):
            execute_coala(
                coala.main, 'coala', '-cc', self.input_toml,
                self.input_toml)

        with self.assertRaises(SystemExit):
            execute_coala(
                coala.main, 'coala', '-cc', self.input_coafile,
                'abc.coafile')

        with self.assertRaises(SystemExit):
            execute_coala(
                coala.main, 'coala', '-cc', 'a.c',
                'b.java'
            )

    def tearDown(self):
        sys.argv = self.old_argv
        os.remove(self.input_coafile)
        os.remove(self.input_toml)
