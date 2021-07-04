import unittest
import tempfile
import os
import logging
from argparse import Namespace

from coala_utils.string_processing import escape
from coalib import coala
from coalib.misc import Constants
from coalib.settings.ConfigGenerator import ConfigGenerator
from tests.TestUtilities import execute_coala


class ConfigGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.config_file = os.path.join(tempfile.gettempdir(), 'temp_file')
        if os.path.sep == '\\':
            self.config_file = escape(self.config_file, '\\')
        self.real_local_coafile = Constants.local_coafile
        Constants.local_coafile = self.config_file
        self.args = Namespace()
        self.uut = ConfigGenerator(self.args)

    def test_creation_with_lang_author(self):
        self.args.generate_config = ['python:pep8', 'cpp:google']

        self.uut.create_coafile()

        with open(self.config_file) as f:
            config_contents = f.read()

        self.assertIn(('[all]\n'
                       '\n'), config_contents)

        self.assertIn(('[all.python]\n'
                       'bears = PEP8Bear, PycodestyleBear\n'
                       'language = Python\n'
                       'files = **\n'
                       'ignore = \n'
                       '\n'), config_contents)

        self.assertIn(('[all.cpp]\n'
                       'bears = CPPLintBear\n'
                       'language = CPP\n'
                       'files = **\n'
                       'ignore = \n'
                       '\n'), config_contents)

    def test_creation_with_lang_auth_file(self):
        self.args.generate_config = ['java:sun:a.java,b.java',
                                     'cpp:apache:c.cpp']
        self.uut.create_coafile()

        with open(self.config_file) as f:
            config_contents = f.read()

        test_file = (
            '[all]\n'
            '\n'
            '[all.java]\n'
            'language = Java\n'
            'bears = CheckstyleBear\n'
            'checkstyle_configs = sun\n'
            'files = a.java,b.java\n'
            'ignore = \n'
            '\n'
        )

        self.assertEqual(test_file, config_contents)

    def test_with_files_args(self):
        self.args.generate_config = ['java:sun:a.java,b.java']
        self.args.files = ['a', 'b', 'c']

        self.uut.create_coafile()

        with open(self.config_file) as f:
            config_contents = f.read()

        test_file = (
            '[all]\n'
            'files = a,b,c\n'
            '\n'
            '[all.java]\n'
            'language = Java\n'
            'bears = CheckstyleBear\n'
            'checkstyle_configs = sun\n'
            'files = a.java,b.java\n'
            'ignore = \n'
            '\n'
        )

        self.assertEqual(test_file, config_contents)

    def test_with_files_and_excludes(self):
        self.args.generate_config = ['java:sun:**:b.java']
        self.uut.create_coafile()

        with open(self.config_file) as f:
            config_contents = f.read()

        test_file = (
            '[all]\n'
            '\n'
            '[all.java]\n'
            'language = Java\n'
            'bears = CheckstyleBear\n'
            'checkstyle_configs = sun\n'
            'files = **\n'
            'ignore = b.java\n'
            '\n'
        )

        self.assertEqual(test_file, config_contents)

    def test_creation_problems(self):
        with self.assertRaises(SystemExit):
            self.args.generate_config = ['java']
            self.uut.create_coafile()

        with self.assertLogs(logging.getLogger(), 'WARNING'):
            self.args.generate_config = ['java:apache']
            self.uut.create_coafile()

    def test_execute_coala(self):
        execute_coala(coala.main, 'coala', '-g', 'python:pep8')

        with open(self.config_file) as f:
            config_content = f.read()

        self.assertEqual(
            config_content,
            '[all]\n'
            '\n'
            '[all.python]\n'
            'bears = PEP8Bear, PycodestyleBear\n'
            'language = Python\n'
            'files = **\n'
            'ignore = \n'
            '\n'
        )

    def tearDown(self):
        Constants.local_coafile = self.real_local_coafile
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
