import copy
import unittest
import os
import tempfile

from coala_utils.string_processing import escape
from coalib.output.TomlConfWriter import TomlConfWriter
from coalib.settings.ConfigurationGathering import load_configuration
from coalib.settings.Section import Section


class TomlConfWriterTest(unittest.TestCase):
    example_file = (
        '[Default]\n'
        '# This is default section\n'
        "files = ['*.py', 'coalib/**/*.py', './coala', 'tests/**/*.py', "
        "'docs/conf.py']\n"
        'ignore = [\n'
        "'tests/bearlib/languages/documentation/"
        "documentation_extraction_testdata/*.py',\n"
        "'tests/collecting/collectors_test_dir/bears/incorrect_bear.py', "
        '#ignore file\n'
        "'coalib/misc/Asyncio.py',] # Files to ignore\n"
        'max_line_length = 80 # Max line length\n'
        'use_spaces = true # A boolean value\n'
        '[python]\n'
        '# Patches may conflict with autopep8 so putting them in own section '
        'so they \n'
        '# will be executed sequentially; also we need the LineLengthBear to '
        'double \n'
        "# check the line length because PEP8Bear sometimes isn't able "
        'to correct the \n'
        '# linelength.\n'
        "bears = ['SpaceConsistencyBear', 'QuotesBear', "
        "'LineContinuationBear']\n"
        "language = 'Python'\n"
        "default_actions = '**: ApplyPatchAction'\n"
        '[flakes]\n'
        '# Do not set default_action to ApplyPatchAction as it may lead '
        'to some \n'
        '# required imports being removed that might result in coala '
        'behaving weirdly. \n'
        "default_actions = '*: ShowPatchAction'\n"
        "bears = 'PyUnusedCodeBear'\n"
        "language = 'Python' # A string\n"
        'remove_all_unused_imports = true \n'
        '[test]\n'
        "inherits = 'python'\n"
        'max = 10\n'
        "appends = 'bears'\n"
        "bears = 'TomlBear'\n"
        '[test2]\n'
        "inherits = ['python', 'flakes']\n"
        "appends.python = 'bears'\n"
        "appends.flakes = 'language'\n"
        "language = 'Toml'\n"
        "bears = 'TomlBear'\n"
        "['another']\n"
        '["another2"]\n'
    )

    result_file = [
        '[python]\n',
        '# Patches may conflict with autopep8 so putting them in own section '
        'so they \n',
        '# will be executed sequentially; also we need the LineLengthBear '
        'to double \n',
        "# check the line length because PEP8Bear sometimes isn't able to "
        'correct the \n',
        '# linelength.\n',
        "bears = ['SpaceConsistencyBear', 'QuotesBear', "
        "'LineContinuationBear']\n",
        "language = 'Python'\n",
        "default_actions = '**: ApplyPatchAction'\n",
        '\n',
        '[flakes]\n',
        '# Do not set default_action to ApplyPatchAction as it may lead '
        'to some \n',
        '# required imports being removed that might result in coala '
        'behaving weirdly. \n',
        "default_actions = '*: ShowPatchAction'\n",
        "bears = 'PyUnusedCodeBear'\n",
        "language = 'Python' # A string\n",
        'remove_all_unused_imports = true \n',
        '\n',
        '[test]\n',
        "inherits = 'python'\n",
        'max = 10\n',
        "appends = 'bears'\n",
        "bears = 'TomlBear'\n",
        '\n',
        '[test2]\n',
        "inherits = ['python', 'flakes']\n",
        "appends.python = 'bears'\n",
        "appends.flakes = 'language'\n",
        "language = 'Toml'\n",
        "bears = 'TomlBear'\n",
        '\n',
        "['another']\n",
        '\n',
        '["another2"]\n',
        '\n',
        '[cli]\n',
        '# This is default section\n',
        "files = ['*.py', 'coalib/**/*.py', './coala', 'tests/**/*.py', "
        "'docs/conf.py']\n",
        'ignore = [\n',
        "'tests/bearlib/languages/documentation/"
        "documentation_extraction_testdata/*.py',\n",
        "'tests/collecting/collectors_test_dir/bears/incorrect_bear.py', "
        '#ignore file\n',
        "'coalib/misc/Asyncio.py',] # Files to ignore\n",
        'max_line_length = 80 # Max line length\n',
        'use_spaces = true # A boolean value\n'
    ]

    def setUp(self):
        self.parse_file = os.path.join(tempfile.gettempdir(),
                                       'TomlConfWriterParseFile')
        self.write_file = os.path.join(tempfile.gettempdir(),
                                       'TomlConfWriterWriteFile')
        with open(self.parse_file, 'w') as file:
            file.write(self.example_file)

        self.uut = TomlConfWriter(self.write_file)

    def tearDown(self):
        os.remove(self.parse_file)
        if os.path.exists(self.write_file):
            os.remove(self.write_file)

    def test_writer(self):
        sections = load_configuration(['-T', '-c',
                                       escape(self.parse_file, '\\')])[0]
        del sections['cli'].contents['config']
        self.uut.write(sections)

        with open(self.write_file, 'r') as f:
            lines = f.readlines()

        self.assertEqual(lines, self.result_file)

    def test_saving(self):
        sections = load_configuration(['-T',
                                       '--bears=SpaceConsistencyBear, TomlBear',
                                       '-S',
                                       'use_file=false',
                                       'a = 10',
                                       '--save',
                                       '-c=' + escape(self.parse_file, '\\'),
                                       ], )[0]

        del sections['cli'].contents['config']

        self.uut.write(sections)
        with open(self.write_file, 'r') as f:
            lines = f.readlines()

        append_file = copy.copy(self.result_file)
        append_file.append('bears = ["SpaceConsistencyBear", "TomlBear"]\n')
        append_file.append('use_file = false\n')
        append_file.append('a = 10\n')
        self.assertEqual(lines, append_file)

    def test_write_with_dir(self):
        self.uut_dir = TomlConfWriter(tempfile.gettempdir())
        self.uut_dir.write({'name': Section('name')})

        with open(os.path.join(tempfile.gettempdir(), '.coafile.toml'),
                  'r') as f:
            lines = f.readlines()

        self.assertEqual(['[name]\n'], lines)
        os.remove(os.path.join(tempfile.gettempdir(), '.coafile.toml'))
