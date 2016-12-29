import logging
import platform
import os
import re
import sys
import unittest
from unittest.mock import ANY, Mock
from unittest.case import skipIf

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
from coalib.settings.Section import Section


def get_testfile_name(name):
    """
    Gets the full path to a testfile inside ``linter_test_files`` directory.

    :param name: The filename of the testfile to get the full path for.
    :return:     The full path to given testfile name.
    """
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'linter_test_files',
                        name)


class LinterComponentTest(unittest.TestCase):

    PARAM_TYPE_ERROR_RE = '[a-z_]+ must be an instance'

    # Using `object` instead of an empty class results in inheritance problems
    # inside the linter decorator.
    class EmptyTestLinter:
        pass

    class RootDirTestLinter:

        def create_arguments(self, *args, **kwargs):
            return tuple()

        def get_config_dir(self):
            return '/'

        def process_output(self, output, *args, **kwargs):
            assert output == '/\n', ("The linter doesn't run the command in "
                                     'the right directory!')

    class ManualProcessingTestLinter:

        def process_output(self, *args, **kwargs):
            pass

    def setUp(self):
        self.section = Section('TEST_SECTION')

    def test_decorator_invalid_parameters(self):
        with self.assertRaises(ValueError) as cm:
            linter('some-executable', invalid_arg=88,
                   ABC=2000)(self.EmptyTestLinter)
        self.assertEqual(
            str(cm.exception),
            "Invalid keyword arguments provided: 'ABC', 'invalid_arg'")

        with self.assertRaises(ValueError) as cm:
            linter('some-executable',
                   diff_severity=RESULT_SEVERITY.MAJOR)(self.EmptyTestLinter)
        self.assertEqual(str(cm.exception),
                         "Invalid keyword arguments provided: 'diff_severity'")

        with self.assertRaises(ValueError) as cm:
            linter('some-executable',
                   result_message='Custom message')(self.EmptyTestLinter)
        self.assertEqual(str(cm.exception),
                         'Invalid keyword arguments provided: '
                         "'result_message'")

        with self.assertRaises(ValueError) as cm:
            linter('some-executable',
                   output_format='corrected',
                   output_regex='.*')(self.EmptyTestLinter)
        self.assertEqual(str(cm.exception),
                         "Invalid keyword arguments provided: 'output_regex'")

        with self.assertRaises(ValueError) as cm:
            linter('some-executable',
                   output_format='corrected',
                   severity_map={})(self.EmptyTestLinter)
        self.assertEqual(str(cm.exception),
                         "Invalid keyword arguments provided: 'severity_map'")

        with self.assertRaises(ValueError) as cm:
            linter('some-executable',
                   prerequisite_check_fail_message='some_message'
                   )(self.EmptyTestLinter)
        self.assertEqual(str(cm.exception),
                         'Invalid keyword arguments provided: '
                         "'prerequisite_check_fail_message'")

    def test_decorator_invalid_states(self):
        with self.assertRaises(ValueError) as cm:
            linter('some-executable', use_stdout=False,
                   use_stderr=False)(self.EmptyTestLinter)
        self.assertEqual(str(cm.exception),
                         'No output streams provided at all.')

        with self.assertRaises(ValueError) as cm:
            linter('some-executable',
                   output_format='INVALID')(self.EmptyTestLinter)
        self.assertEqual(str(cm.exception),
                         'Invalid `output_format` specified.')

        with self.assertRaises(ValueError) as cm:
            linter('some-executable',
                   output_format='regex')(self.EmptyTestLinter)
        self.assertEqual(
            str(cm.exception),
            "`output_regex` needed when specified output-format 'regex'.")

        with self.assertRaises(ValueError) as cm:
            linter('some-executable',
                   output_format='regex',
                   output_regex='',
                   severity_map={})(self.EmptyTestLinter)
        self.assertEqual(
            str(cm.exception),
            'Provided `severity_map` but named group `severity` is not used '
            'in `output_regex`.')

        with self.assertRaises(ValueError) as cm:
            linter('some-executable')(object)
        self.assertEqual(
            str(cm.exception),
            "`process_output` not provided by given class 'object'.")

        with self.assertRaises(ValueError) as cm:
            (linter('some-executable', output_format='regex', output_regex='')
             (self.ManualProcessingTestLinter))
        self.assertEqual(
            str(cm.exception),
            'Found `process_output` already defined by class '
            "'ManualProcessingTestLinter', but 'regex' output-format is "
            'specified.')

    def test_decorator_generated_default_interface(self):
        uut = linter('some-executable')(self.ManualProcessingTestLinter)
        with self.assertRaisesRegex(NotImplementedError, ''):
            uut.create_arguments('filename', 'content', None)

    def test_decorator_invalid_parameter_types(self):
        # Provide some invalid severity maps.
        with self.assertRaisesRegex(TypeError, self.PARAM_TYPE_ERROR_RE):
            linter('some-executable',
                   output_format='regex',
                   output_regex='(?P<severity>)',
                   severity_map=list())(self.EmptyTestLinter)

        with self.assertRaisesRegex(TypeError, self.PARAM_TYPE_ERROR_RE):
            linter('some-executable',
                   output_format='regex',
                   output_regex='(?P<severity>)',
                   severity_map={3: 0})(self.EmptyTestLinter)

        with self.assertRaises(TypeError) as cm:
            linter('some-executable',
                   output_format='regex',
                   output_regex='(?P<severity>)',
                   severity_map={'critical': 'invalid'})(self.EmptyTestLinter)
        self.assertEqual(str(cm.exception),
                         "The value 'invalid' for key 'critical' inside given "
                         'severity-map is no valid severity value.')

        with self.assertRaises(TypeError) as cm:
            linter('some-executable',
                   output_format='regex',
                   output_regex='(?P<severity>)',
                   severity_map={'critical-error': 389274234})(
                   self.EmptyTestLinter)
        self.assertEqual(str(cm.exception),
                         'Invalid severity value 389274234 for key '
                         "'critical-error' inside given severity-map.")

        # Other type-error test cases.

        with self.assertRaisesRegex(TypeError, self.PARAM_TYPE_ERROR_RE):
            linter('some-executable',
                   output_format='regex',
                   output_regex='(?P<message>)',
                   result_message=None)(self.EmptyTestLinter)

        with self.assertRaisesRegex(TypeError, self.PARAM_TYPE_ERROR_RE):
            linter('some-executable',
                   output_format='corrected',
                   result_message=list())(self.EmptyTestLinter)

        with self.assertRaises(TypeError) as cm:
            linter('some-executable',
                   output_format='corrected',
                   diff_severity=999888777)(self.EmptyTestLinter)
        self.assertEqual(str(cm.exception),
                         'Invalid value for `diff_severity`: 999888777')

        with self.assertRaisesRegex(TypeError, self.PARAM_TYPE_ERROR_RE):
            linter('some-executable',
                   prerequisite_check_command=('command',),
                   prerequisite_check_fail_message=382983)(self.EmptyTestLinter)

    def test_get_executable(self):
        uut = linter('some-executable')(self.ManualProcessingTestLinter)
        self.assertEqual(uut.get_executable(), 'some-executable')

    def test_check_prerequisites(self):
        uut = linter(sys.executable)(self.ManualProcessingTestLinter)
        self.assertTrue(uut.check_prerequisites())

        uut = (linter('invalid_nonexisting_programv412')
               (self.ManualProcessingTestLinter))
        self.assertEqual(uut.check_prerequisites(),
                         "'invalid_nonexisting_programv412' is not installed.")

        uut = (linter('invalid_nonexisting_programv412',
                      executable_check_fail_info="You can't install it.")
               (self.ManualProcessingTestLinter))
        self.assertEqual(uut.check_prerequisites(),
                         "'invalid_nonexisting_programv412' is not installed. "
                         "You can't install it.")

        uut = (linter(sys.executable,
                      prerequisite_check_command=(sys.executable, '--version'))
               (self.ManualProcessingTestLinter))
        self.assertTrue(uut.check_prerequisites())

        uut = (linter(sys.executable,
                      prerequisite_check_command=('invalid_programv413',))
               (self.ManualProcessingTestLinter))
        self.assertEqual(uut.check_prerequisites(),
                         'Prerequisite check failed.')

        uut = (linter(sys.executable,
                      prerequisite_check_command=('invalid_programv413',),
                      prerequisite_check_fail_message='NOPE')
               (self.ManualProcessingTestLinter))
        self.assertEqual(uut.check_prerequisites(), 'NOPE')

    def test_output_stream(self):
        process_output_mock = Mock()

        class TestLinter:

            @staticmethod
            def process_output(output, filename, file):
                process_output_mock(output, filename, file)

            @staticmethod
            def create_arguments(filename, file, config_file):
                code = '\n'.join(['import sys',
                                  "print('hello stdout')",
                                  "print('hello stderr', file=sys.stderr)"])
                return '-c', code

        uut = (linter(sys.executable, use_stdout=True)
               (TestLinter)
               (self.section, None))
        uut.run('', [])

        process_output_mock.assert_called_once_with('hello stdout\n', '', [])
        process_output_mock.reset_mock()

        uut = (linter(sys.executable, use_stdout=False, use_stderr=True)
               (TestLinter)
               (self.section, None))
        uut.run('', [])

        process_output_mock.assert_called_once_with('hello stderr\n', '', [])
        process_output_mock.reset_mock()

        uut = (linter(sys.executable, use_stdout=True, use_stderr=True)
               (TestLinter)
               (self.section, None))

        uut.run('', [])

        process_output_mock.assert_called_once_with(('hello stdout\n',
                                                     'hello stderr\n'), '', [])

    def test_process_output_corrected(self):
        uut = (linter(sys.executable, output_format='corrected')
               (self.EmptyTestLinter)
               (self.section, None))

        original = ['void main()  {\n', 'return 09;\n', '}\n']
        fixed = ['void main()\n', '{\n', 'return 9;\n', '}\n']
        fixed_string = ''.join(fixed)

        results = list(uut.process_output(fixed_string,
                                          'some-file.c',
                                          original))

        diffs = list(Diff.from_string_arrays(original, fixed).split_diff())
        expected = [Result.from_values(uut,
                                       'Inconsistency found.',
                                       'some-file.c',
                                       1, None, 2, None,
                                       RESULT_SEVERITY.NORMAL,
                                       diffs={'some-file.c': diffs[0]})]

        self.assertEqual(results, expected)

        # Test when providing a sequence as output.

        results = list(uut.process_output([fixed_string, fixed_string],
                                          'some-file.c',
                                          original))
        self.assertEqual(results, 2 * expected)

        # Test diff_distance

        uut = (linter(sys.executable,
                      output_format='corrected',
                      diff_distance=-1)
               (self.EmptyTestLinter)
               (self.section, None))

        results = list(uut.process_output(fixed_string,
                                          'some-file.c',
                                          original))
        self.assertEqual(len(results), 2)

    def test_process_output_regex(self):
        # Also test the case when an unknown severity is matched.
        test_output = ('12:4-14:0-Serious issue (error) -> ORIGIN=X -> D\n'
                       '0:0-0:1-This is a warning (warning) -> ORIGIN=Y -> A\n'
                       '813:77-1024:32-Just a note (info) -> ORIGIN=Z -> C\n'
                       '0:0-0:0-Some unknown sev (???) -> ORIGIN=W -> B\n')
        regex = (r'(?P<line>\d+):(?P<column>\d+)-'
                 r'(?P<end_line>\d+):(?P<end_column>\d+)-'
                 r'(?P<message>.*) \((?P<severity>.*)\) -> '
                 r'ORIGIN=(?P<origin>.*) -> (?P<additional_info>.*)')

        uut = (linter(sys.executable,
                      output_format='regex',
                      output_regex=regex)
               (self.EmptyTestLinter)
               (self.section, None))
        uut.warn = Mock()

        sample_file = 'some-file.xtx'
        results = list(uut.process_output(test_output, sample_file, ['']))
        expected = [Result.from_values('EmptyTestLinter (X)',
                                       'Serious issue',
                                       sample_file,
                                       12, 4, 14, 0,
                                       RESULT_SEVERITY.MAJOR,
                                       additional_info='D'),
                    Result.from_values('EmptyTestLinter (Y)',
                                       'This is a warning',
                                       sample_file,
                                       0, 0, 0, 1,
                                       RESULT_SEVERITY.NORMAL,
                                       additional_info='A'),
                    Result.from_values('EmptyTestLinter (Z)',
                                       'Just a note',
                                       sample_file,
                                       813, 77, 1024, 32,
                                       RESULT_SEVERITY.INFO,
                                       additional_info='C'),
                    Result.from_values('EmptyTestLinter (W)',
                                       'Some unknown sev',
                                       sample_file,
                                       0, 0, 0, 0,
                                       RESULT_SEVERITY.NORMAL,
                                       additional_info='B')]

        self.assertEqual(results, expected)
        uut.warn.assert_called_once_with(
            "'???' not found in severity-map. Assuming "
            '`RESULT_SEVERITY.NORMAL`.')

        # Test when providing a sequence as output.
        test_output = ['',
                       '12:4-14:0-Serious issue (error) -> ORIGIN=X -> XYZ\n']
        results = list(uut.process_output(test_output, sample_file, ['']))
        expected = [Result.from_values('EmptyTestLinter (X)',
                                       'Serious issue',
                                       sample_file,
                                       12, 4, 14, 0,
                                       RESULT_SEVERITY.MAJOR,
                                       additional_info='XYZ')]

        self.assertEqual(results, expected)

        # Test with using `result_message` parameter.
        uut = (linter(sys.executable,
                      output_format='regex',
                      output_regex=regex,
                      result_message='Hello world')
               (self.EmptyTestLinter)
               (self.section, None))

        results = list(uut.process_output(test_output, sample_file, ['']))
        expected = [Result.from_values('EmptyTestLinter (X)',
                                       'Hello world',
                                       sample_file,
                                       12, 4, 14, 0,
                                       RESULT_SEVERITY.MAJOR,
                                       additional_info='XYZ')]

        self.assertEqual(results, expected)

    def test_minimal_regex(self):
        uut = (linter(sys.executable,
                      output_format='regex',
                      output_regex='an_issue')
               (self.EmptyTestLinter)
               (self.section, None))

        results = list(uut.process_output(['not an issue'], 'file', ['']))
        self.assertEqual(results, [])

        results = list(uut.process_output(['an_issue'], 'file', ['']))
        self.assertEqual(results, [Result.from_values('EmptyTestLinter', '',
                                                      file='file')])

    def test_get_non_optional_settings(self):
        class Handler(self.ManualProcessingTestLinter):

            @staticmethod
            def create_arguments(filename, file, config_file, param_x: int):
                pass

            @staticmethod
            def generate_config(filename, file, superparam):
                """
                :param superparam: A superparam!
                """
                return None

        uut = linter(sys.executable)(Handler)

        self.assertEqual(uut.get_non_optional_settings(),
                         {'param_x': ('No description given.', int),
                          'superparam': ('A superparam!', None)})

    def test_process_output_metadata_omits_on_builtin_formats(self):
        uut = (linter(executable='', output_format='corrected')
               (self.EmptyTestLinter))
        # diff_severity and result_message should now not occur inside the
        # metadata definition.
        self.assertNotIn('diff_severity', uut.get_metadata().optional_params)
        self.assertNotIn('result_message', uut.get_metadata().optional_params)
        self.assertNotIn('diff_severity',
                         uut.get_metadata().non_optional_params)
        self.assertNotIn('result_message',
                         uut.get_metadata().non_optional_params)

        # But every parameter manually defined in process_output shall appear
        # inside the metadata signature.
        class Handler:

            @staticmethod
            def create_arguments(filename, file, config_file):
                pass

            @staticmethod
            def process_output(output, filename, file, diff_severity):
                pass

        uut = linter(executable='')(Handler)
        self.assertIn('diff_severity', uut.get_metadata().non_optional_params)

    def test_section_settings_forwarding(self):
        create_arguments_mock = Mock()
        generate_config_mock = Mock()
        process_output_mock = Mock()

        class Handler(self.ManualProcessingTestLinter):

            @staticmethod
            def create_arguments(filename, file, config_file, my_param: int):
                create_arguments_mock(filename, file, config_file, my_param)
                # Execute python and do nothing.
                return '-c', "print('coala!')"

            @staticmethod
            def generate_config(filename, file, my_config_param: int):
                generate_config_mock(filename, file, my_config_param)
                return None

            def process_output(self, output, filename, file, makman2: str):
                process_output_mock(output, filename, file, makman2)

        self.section['my_param'] = '109'
        self.section['my_config_param'] = '88'
        self.section['makman2'] = 'is cool'

        uut = linter(sys.executable)(Handler)(self.section, None)

        self.assertIsNotNone(list(uut.execute(filename='some_file.cs',
                                              file=[])))
        create_arguments_mock.assert_called_once_with(
            'some_file.cs', [], None, 109)
        generate_config_mock.assert_called_once_with('some_file.cs', [], 88)
        process_output_mock.assert_called_once_with(
            'coala!\n', 'some_file.cs', [], 'is cool')

    def test_section_settings_defaults_forwarding(self):
        create_arguments_mock = Mock()
        generate_config_mock = Mock()
        process_output_mock = Mock()

        class Handler:

            @staticmethod
            def generate_config(filename, file, some_default: str='x'):
                generate_config_mock(filename, file, some_default)
                return None

            @staticmethod
            def create_arguments(filename, file, config_file, default: int=3):
                create_arguments_mock(
                    filename, file, config_file, default)
                return '-c', "print('hello')"

            @staticmethod
            def process_output(output, filename, file, xxx: int=64):
                process_output_mock(output, filename, file, xxx)

        uut = linter(sys.executable)(Handler)(self.section, None)

        self.assertIsNotNone(list(uut.execute(filename='abc.py', file=[])))
        create_arguments_mock.assert_called_once_with('abc.py', [], None, 3)
        generate_config_mock.assert_called_once_with('abc.py', [], 'x')
        process_output_mock.assert_called_once_with(
            'hello\n', 'abc.py', [], 64)

        create_arguments_mock.reset_mock()
        generate_config_mock.reset_mock()
        process_output_mock.reset_mock()

        self.section['default'] = '1000'
        self.section['some_default'] = 'xyz'
        self.section['xxx'] = '-50'
        self.assertIsNotNone(list(uut.execute(filename='def.py', file=[])))
        create_arguments_mock.assert_called_once_with('def.py', [], None, 1000)
        generate_config_mock.assert_called_once_with('def.py', [], 'xyz')
        process_output_mock.assert_called_once_with(
            'hello\n', 'def.py', [], -50)

    def test_invalid_arguments(self):

        class InvalidArgumentsLinter(self.ManualProcessingTestLinter):

            @staticmethod
            def create_arguments(filename, file, config_file):
                return None

        uut = (linter(sys.executable)(InvalidArgumentsLinter)
               (self.section, None))
        self.assertEqual(uut.run('', []), None)

    def test_generate_config(self):
        uut = linter('')(self.ManualProcessingTestLinter)
        with uut._create_config('filename', []) as config_file:
            self.assertIsNone(config_file)

        class ConfigurationTestLinter(self.ManualProcessingTestLinter):

            @staticmethod
            def generate_config(filename, file, val):
                return 'config_value = ' + str(val)

        uut = linter('', config_suffix='.xml')(ConfigurationTestLinter)
        with uut._create_config('filename', [], val=88) as config_file:
            self.assertTrue(os.path.isfile(config_file))
            self.assertEqual(config_file[-4:], '.xml')
            with open(config_file, mode='r') as fl:
                self.assertEqual(fl.read(), 'config_value = 88')
        self.assertFalse(os.path.isfile(config_file))

    def test_metaclass_repr(self):
        uut = linter('my-tool')(self.ManualProcessingTestLinter)
        self.assertEqual(
            repr(uut),
            "<ManualProcessingTestLinter linter class (wrapping 'my-tool')>")

        # Test also whether derivatives change the class name accordingly.
        class DerivedLinter(uut):
            pass
        self.assertEqual(repr(DerivedLinter),
                         "<DerivedLinter linter class (wrapping 'my-tool')>")

    def test_repr(self):
        uut = (linter(sys.executable)
               (self.ManualProcessingTestLinter)
               (self.section, None))

        self.assertRegex(
            repr(uut),
            '<ManualProcessingTestLinter linter object \\(wrapping ' +
            re.escape(repr(sys.executable)) + '\\) at 0x[a-fA-F0-9]+>')

    @skipIf(platform.system() == 'Windows',
            '`pwd` does not exist in Windows-cmd and `cd` is a built-in '
            'command which fails the executable-existence check from @linter.')
    def test_process_directory(self):
        """
        The linter shall run the process in the right directory so tools can
        use the current working directory to resolve import like things.
        """
        uut = (linter('pwd')
               (self.RootDirTestLinter)
               (self.section, None))
        uut.run('', [])  # Does an assert in the output processing


class LinterReallifeTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('REALLIFE_TEST_SECTION')

        self.test_program_path = get_testfile_name('test_linter.py')
        self.test_program_regex = (
            r'L(?P<line>\d+)C(?P<column>\d+)-'
            r'L(?P<end_line>\d+)C(?P<end_column>\d+):'
            r' (?P<message>.*) \| (?P<severity>.+) SEVERITY')
        self.test_program_severity_map = {'MAJOR': RESULT_SEVERITY.MAJOR}

        self.testfile_path = get_testfile_name('test_file.txt')
        with open(self.testfile_path, mode='r') as fl:
            self.testfile_content = fl.read().splitlines(keepends=True)

        self.testfile2_path = get_testfile_name('test_file2.txt')
        with open(self.testfile2_path, mode='r') as fl:
            self.testfile2_content = fl.read().splitlines(keepends=True)

    def test_nostdin_nostderr_noconfig_nocorrection(self):
        create_arguments_mock = Mock()

        class Handler:

            @staticmethod
            def create_arguments(filename, file, config_file):
                create_arguments_mock(filename, file, config_file)
                return self.test_program_path, filename

        uut = (linter(sys.executable,
                      output_format='regex',
                      output_regex=self.test_program_regex,
                      severity_map=self.test_program_severity_map)
               (Handler)
               (self.section, None))

        results = list(uut.run(self.testfile_path, self.testfile_content))
        expected = [Result.from_values(uut,
                                       "Invalid char ('0')",
                                       self.testfile_path,
                                       3, 0, 3, 1,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values(uut,
                                       "Invalid char ('.')",
                                       self.testfile_path,
                                       5, 0, 5, 1,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values(uut,
                                       "Invalid char ('p')",
                                       self.testfile_path,
                                       9, 0, 9, 1,
                                       RESULT_SEVERITY.MAJOR)]

        self.assertEqual(results, expected)
        create_arguments_mock.assert_called_once_with(
            self.testfile_path, self.testfile_content, None)

    def test_stdin_stderr_noconfig_nocorrection(self):
        create_arguments_mock = Mock()

        class Handler:

            @staticmethod
            def create_arguments(filename, file, config_file):
                create_arguments_mock(filename, file, config_file)
                return (self.test_program_path,
                        '--use_stderr',
                        '--use_stdin',
                        filename)

        uut = (linter(sys.executable,
                      use_stdin=True,
                      use_stdout=False,
                      use_stderr=True,
                      output_format='regex',
                      output_regex=self.test_program_regex,
                      severity_map=self.test_program_severity_map)
               (Handler)
               (self.section, None))

        results = list(uut.run(self.testfile2_path, self.testfile2_content))
        expected = [Result.from_values(uut,
                                       "Invalid char ('X')",
                                       self.testfile2_path,
                                       0, 0, 0, 1,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values(uut,
                                       "Invalid char ('i')",
                                       self.testfile2_path,
                                       4, 0, 4, 1,
                                       RESULT_SEVERITY.MAJOR)]

        self.assertEqual(results, expected)
        create_arguments_mock.assert_called_once_with(
            self.testfile2_path, self.testfile2_content, None)

    def test_nostdin_nostderr_noconfig_correction(self):
        create_arguments_mock = Mock()

        class Handler:

            @staticmethod
            def create_arguments(filename, file, config_file):
                create_arguments_mock(filename, file, config_file)
                return self.test_program_path, '--correct', filename

        uut = (linter(sys.executable,
                      output_format='corrected',
                      diff_severity=RESULT_SEVERITY.INFO,
                      result_message='Custom message')
               (Handler)
               (self.section, None))

        results = list(uut.run(self.testfile_path, self.testfile_content))

        expected_correction = [s + '\n'
                               for s in ['+', '-', '*', '++', '-', '-', '+']]

        diffs = list(Diff.from_string_arrays(
            self.testfile_content,
            expected_correction).split_diff())

        expected = [Result(uut, 'Custom message',
                           affected_code=(
                               SourceRange.from_values(self.testfile_path, 4),
                               SourceRange.from_values(self.testfile_path, 6)),
                           severity=RESULT_SEVERITY.INFO,
                           diffs={self.testfile_path: diffs[0]}),
                    Result.from_values(uut,
                                       'Custom message',
                                       self.testfile_path,
                                       10, None, 10, None,
                                       RESULT_SEVERITY.INFO,
                                       diffs={self.testfile_path: diffs[1]})]

        self.assertEqual(results, expected)
        create_arguments_mock.assert_called_once_with(
            self.testfile_path, self.testfile_content, None)

    def test_stdin_stdout_stderr_config_nocorrection(self):
        create_arguments_mock = Mock()
        generate_config_mock = Mock()

        class Handler:

            @staticmethod
            def generate_config(filename, file, some_val):
                # some_val shall only test the argument delegation from run().
                generate_config_mock(filename, file, some_val)
                return '\n'.join(['use_stdin', 'use_stderr'])

            @staticmethod
            def create_arguments(filename, file, config_file, some_val):
                create_arguments_mock(filename, file, config_file, some_val)
                return self.test_program_path, '--config', config_file

        uut = (linter(sys.executable,
                      use_stdin=True,
                      use_stderr=True,
                      output_format='regex',
                      output_regex=self.test_program_regex,
                      severity_map=self.test_program_severity_map,
                      result_message='Invalid char provided!')
               (Handler)
               (self.section, None))

        results = list(uut.run(self.testfile_path,
                               self.testfile_content,
                               some_val=33))
        expected = [Result.from_values(uut,
                                       'Invalid char provided!',
                                       self.testfile_path,
                                       3, 0, 3, 1,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values(uut,
                                       'Invalid char provided!',
                                       self.testfile_path,
                                       5, 0, 5, 1,
                                       RESULT_SEVERITY.MAJOR),
                    Result.from_values(uut,
                                       'Invalid char provided!',
                                       self.testfile_path,
                                       9, 0, 9, 1,
                                       RESULT_SEVERITY.MAJOR)]

        self.assertEqual(results, expected)
        create_arguments_mock.assert_called_once_with(
            self.testfile_path, self.testfile_content, ANY, 33)
        self.assertIsNotNone(create_arguments_mock.call_args[0][2])
        generate_config_mock.assert_called_once_with(
            self.testfile_path, self.testfile_content, 33)

    def test_stdin_stderr_config_correction(self):
        create_arguments_mock = Mock()
        generate_config_mock = Mock()

        # `some_value_A` and `some_value_B` are used to test the different
        # delegation to `generate_config()` and `create_arguments()`
        # accordingly.
        class Handler:

            @staticmethod
            def generate_config(filename, file, some_value_A):
                generate_config_mock(filename, file, some_value_A)
                return '\n'.join(['use_stdin', 'use_stderr', 'correct'])

            @staticmethod
            def create_arguments(filename, file, config_file, some_value_B):
                create_arguments_mock(filename, file, config_file,
                                      some_value_B)
                return self.test_program_path, '--config', config_file

        uut = (linter(sys.executable,
                      use_stdin=True,
                      use_stdout=False,
                      use_stderr=True,
                      output_format='corrected',
                      config_suffix='.conf')
               (Handler)
               (self.section, None))

        results = list(uut.run(self.testfile2_path,
                               self.testfile2_content,
                               some_value_A=124,
                               some_value_B=-78))

        expected_correction = [s + '\n' for s in ['+', '/', '/', '-']]

        diffs = list(Diff.from_string_arrays(
            self.testfile2_content,
            expected_correction).split_diff())

        expected = [Result.from_values(uut,
                                       'Inconsistency found.',
                                       self.testfile2_path,
                                       1, None, 1, None,
                                       RESULT_SEVERITY.NORMAL,
                                       diffs={self.testfile2_path: diffs[0]}),
                    Result.from_values(uut,
                                       'Inconsistency found.',
                                       self.testfile2_path,
                                       5, None, 5, None,
                                       RESULT_SEVERITY.NORMAL,
                                       diffs={self.testfile2_path: diffs[1]})]

        self.assertEqual(results, expected)
        create_arguments_mock.assert_called_once_with(
            self.testfile2_path, self.testfile2_content, ANY, -78)
        self.assertEqual(create_arguments_mock.call_args[0][2][-5:], '.conf')
        generate_config_mock.assert_called_once_with(
            self.testfile2_path, self.testfile2_content, 124)

    def test_capture_groups_warnings(self):
        logger = logging.getLogger()
        with self.assertLogs(logger, 'WARNING') as cm:
            @linter('some-executable',
                    use_stdout=True,
                    output_format='regex',
                    output_regex=r'(?P<not_supported_name>)\d+(\w+)')
            class SomeBear:
                pass

        self.assertEqual(cm.output, [
            'WARNING:root:SomeBear: Using unnecessary capturing groups '
            'affects the performance of coala. '
            "You should use '(?:<pattern>)' instead of "
            "'(<pattern>)' for your regex.",

            'WARNING:root:SomeBear: Superfluous capturing group '
            "'not_supported_name' used. Is this a typo? If not, consider "
            "removing the capturing group to improve coala's "
            'performance.'])
