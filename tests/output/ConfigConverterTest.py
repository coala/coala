import unittest
import os
import tempfile

from coalib.output.ConfigConverter import ConfigConverter
from coalib.settings.ConfigurationGathering import (
    load_config_file, load_toml_config_file)


class ConfigConverterTest(unittest.TestCase):
    coafile = """
[Default]
bears = TestBear

[all]
files = *.py, coantlib/**/*.py, tests/**/*.py, coantbears/**/*.py, .ci/*.py
ignore =
    coantlib/coantparsers/**.py,
    tests/files/**.py
max_line_length = 80
use_spaces = True
bears += SpaceConsistencyBear

[all.python]
# Patches may conflict with autopep8 so putting them in own section so they
bears += PyBear
language = Python

[flakes.python]
language += test

[all.toml]
bears += TomlBear
language = Python
default_actions = **: ApplyPatchAction
"""

    coafile_2 = """[all]
files = *.py, coantlib/**/*.py, tests/**/*.py, coantbears/**/*.py, .ci/*.py
ignore =
    coantlib/coantparsers/**.py,
    tests/files/**.py
max_line_length = 80
use_spaces = True
bears = SpaceConsistencyBear

[all.python]
# Patches may conflict with autopep8 so putting them in own section so they
bears += PyBear
language = Python

[flakes.python]
language += test

[all.toml]
bears += TomlBear
language = Python
default_actions = **: ApplyPatchAction
"""

    toml_file = """[Default]
l = '3'

[a]
# A section
p = '10'
q = '20'
l = '3'
appends = 'l'
save = true

[b]
c = '5'
d  = '6'

[c]
inherits = [ 'a', 'b' ]
p  = '12'
d  = '14'
appends.a = 'p'
appends.b = 'd'
"""

    def setUp(self):
        self.toml_input_file = os.path.join(tempfile.gettempdir(),
                                            'in.toml')
        self.coafile_input_file = os.path.join(tempfile.gettempdir(),
                                               'in_file')
        with open(self.toml_input_file, 'w') as f:
            f.write(self.toml_file)
        with open(self.coafile_input_file, 'w') as f:
            f.write(self.coafile)

    def tearDown(self):
        os.remove(self.toml_input_file)
        os.remove(self.coafile_input_file)

    def test_coafile_to_toml(self):
        output = ['[all]\n',
                  'files = ["*.py", "coantlib/**/*.py", "tests/**/*.py", '
                  '"coantbears/**/*.py", ".ci/*.py"]\n',
                  'ignore = ["coantlib/coantparsers/**.py", '
                  '"tests/files/**.py"]\n',
                  'max_line_length = 80\n',
                  'use_spaces = true\n',
                  'bears = "SpaceConsistencyBear"\n',
                  'appends = ["bears"]\n',
                  '\n',
                  '[python]\n',
                  'bears = "PyBear"\n',
                  'language = "Python"\n',
                  'inherits = ["all", "flakes"]\n',
                  'appends.all = ["bears"]\n',
                  'appends.flakes = ["language"]\n',
                  '\n',
                  '[toml]\n',
                  'bears = "TomlBear"\n',
                  'language = "Python"\n',
                  'default_actions = "**: ApplyPatchAction"\n',
                  'inherits = ["all"]\n',
                  'appends.all = ["bears"]\n',
                  '\n',
                  '[cli]\n',
                  'bears = "TestBear"\n',
                  ]

        sections = load_config_file(self.coafile_input_file)
        toml_output_file = os.path.join(tempfile.gettempdir(),
                                        'out.toml')
        uut_toml = ConfigConverter(toml_output_file)
        uut_toml.coafile_to_toml(sections)
        with open(toml_output_file, 'r') as f:
            lines = f.readlines()
        os.remove(toml_output_file)
        self.assertEqual(lines, output)

    def test_coafile_to_toml_without_default(self):
        output = ['[all]\n',
                  'files = ["*.py", "coantlib/**/*.py", "tests/**/*.py", '
                  '"coantbears/**/*.py", ".ci/*.py"]\n',
                  'ignore = ["coantlib/coantparsers/**.py", '
                  '"tests/files/**.py"]\n',
                  'max_line_length = 80\n',
                  'use_spaces = true\n',
                  'bears = "SpaceConsistencyBear"\n',
                  '\n',
                  '[python]\n',
                  'bears = "PyBear"\n',
                  'language = "Python"\n',
                  'inherits = ["all", "flakes"]\n',
                  'appends.all = ["bears"]\n',
                  'appends.flakes = ["language"]\n',
                  '\n',
                  '[toml]\n',
                  'bears = "TomlBear"\n',
                  'language = "Python"\n',
                  'default_actions = "**: ApplyPatchAction"\n',
                  'inherits = ["all"]\n',
                  'appends.all = ["bears"]\n'
                  ]

        with open(self.coafile_input_file, 'w') as f:
            f.write(self.coafile_2)
        out_file = os.path.join(tempfile.gettempdir(), 'out.toml')
        uut_toml = ConfigConverter(out_file)
        sections = load_config_file(self.coafile_input_file)
        del sections['default']
        uut_toml.coafile_to_toml(sections)
        with open(out_file, 'r') as f:
            lines = f.readlines()
        os.remove(out_file)
        self.assertEqual(lines, output)

    def test_toml_to_coafile(self):
        output = ['[a]\n',
                  'p = 10\n',
                  'q = 20\n',
                  'l += 3\n',
                  '\n',
                  '[b]\n',
                  'c = 5\n',
                  'd = 6\n',
                  '\n',
                  '[a.c]\n',
                  'p += 12\n',
                  'd = 14\n',
                  '[b.c]\n',
                  'p = 12\n',
                  'd += 14\n',
                  '[cli]\n',
                  'l = 3\n',
                  '\n']

        sections = load_toml_config_file(self.toml_input_file)
        coafile_output_file = os.path.join(tempfile.gettempdir(),
                                           'out_file')
        uut_coafile = ConfigConverter(coafile_output_file)
        uut_coafile.toml_to_coafile(sections)
        with open(coafile_output_file, 'r') as f:
            lines = f.readlines()
        os.remove(coafile_output_file)
        self.assertEqual(lines, output)
