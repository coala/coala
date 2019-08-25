import pdb
import os
from collections import defaultdict
import datetime
from io import BytesIO, StringIO
import multiprocessing
import unittest
from os.path import abspath, exists, isfile, join, getmtime
from tempfile import TemporaryDirectory, NamedTemporaryFile
import shutil

from freezegun import freeze_time
from unittest.mock import patch

import requests
import requests_mock

from coalib.coala_main import run_coala
from coalib.bearlib.aspects.collections import AspectList
from coalib.bearlib.aspects.Metadata import CommitMessage
from coalib.bearlib.languages.Language import Language, Languages
from coalib.bears.Bear import (
    Bear, Debugger, _setting_is_enabled, _is_debugged, _is_profiled)
from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.TextPosition import ZeroOffsetError
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.processes.communication.LogMessage import LogMessage
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting, language
from pyprint.ConsolePrinter import ConsolePrinter
from coala_utils.ContextManagers import prepare_file

from tests.TestUtilities import bear_test_module


class BadTestBear(Bear):

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    @staticmethod
    def kind():
        return BEAR_KIND.GLOBAL

    def run(self):
        raise NotImplementedError


class TestBear(Bear):

    BEAR_DEPS = {BadTestBear}

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    @staticmethod
    def kind():
        return BEAR_KIND.GLOBAL

    def run(self):
        self.print('set', 'up', delimiter='=')
        self.err('teardown')
        self.err()


class TestOneBear(LocalBear):
    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def run(self, x: int, y: str, z: int = 79, w: str = 'kbc'):
        yield 1
        yield 2


class TestTwoBear(Bear):

    def run(self, *args, **kwargs):
        yield 1
        yield 2
        yield 3


class TestThreeBear(Bear):

    def run(self, *args, **kwargs):
        pass


class TypedTestBear(Bear):

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)
        self.was_executed = False

    def run(self, something: int):
        self.was_executed = True
        return []


class ZeroOffsetLocalBear(LocalBear):

    def __init__(self, section, queue, error_message):
        Bear.__init__(self, section, queue)
        self.error_message = error_message

    def run(self, filename, file):
        raise ZeroOffsetError(self.error_message)


class ZeroOffsetGlobalBear(Bear):

    def __init__(self, section, queue, error_message):
        Bear.__init__(self, section, queue)
        self.error_message = error_message

    @staticmethod
    def kind():
        return BEAR_KIND.GLOBAL

    def run(self):
        raise ZeroOffsetError(self.error_message)


class BearWithPrerequisites(Bear):
    prerequisites_fulfilled = True

    def __init__(self, section, queue, prerequisites_fulfilled):
        BearWithPrerequisites.prerequisites_fulfilled = prerequisites_fulfilled
        Bear.__init__(self, section, queue)
        self.was_executed = False

    def run(self):
        self.was_executed = True
        return []

    @classmethod
    def check_prerequisites(cls):
        return cls.prerequisites_fulfilled


class StandAloneBear(Bear):

    def run(self, x: int, y: int, z: int = 33):
        """
        Test run.
        :param x: First value.
        :param y: Second value.
        :param z: Third value.
        """
        yield x
        yield y
        yield z


class DependentBear(Bear):

    BEAR_DEPS = {StandAloneBear}

    def run(self, y: int, w: float):
        """
        Test run with more params.
        :param y: Second value, but better.
        :param w: Fourth value.
        """
        yield y
        yield w


class aspectsTestBear(Bear, aspects={
        'detect': [CommitMessage.Shortlog.ColonExistence],
        'fix': [CommitMessage.Shortlog.TrailingPeriod],
}, languages=['Python', 'C#']):
    pass


class aspectsDetectOnlyTestBear(Bear, aspects={
        'detect': [CommitMessage.Shortlog.ColonExistence],
}, languages=['Python']):
    pass


class aspectsFixOnlyTestBear(Bear, aspects={
        'fix': [CommitMessage.Shortlog.TrailingPeriod],
}, languages=['Python']):
    pass


class BearWithLanguage(Bear):

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    @staticmethod
    def kind():
        return BEAR_KIND.GLOBAL

    def run(self, language: language = language('Python 3.4')):
        yield language


class BearTestBase(unittest.TestCase):

    def setUp(self):
        self.queue = multiprocessing.Queue()
        self.settings = Section('test_settings')
        self.uut = TestBear(self.settings, self.queue)

    def tearDown(self):
        if exists(self.uut.data_dir):
            shutil.rmtree(self.uut.data_dir)


class BearTest(BearTestBase):

    def test_languages(self):
        self.assertIs(type(aspectsTestBear.languages), Languages)
        self.assertIn('Python', aspectsTestBear.languages)
        self.assertIn('csharp', aspectsTestBear.languages)
        self.assertNotIn('javascript', aspectsTestBear.languages)

    def test_default_aspects(self):
        assert type(Bear.aspects) is defaultdict
        assert type(Bear.aspects['detect']) is AspectList
        assert type(Bear.aspects['fix']) is AspectList
        assert Bear.aspects['detect'] == Bear.aspects['fix'] == []

    def test_no_fix_aspects(self):
        assert type(aspectsDetectOnlyTestBear.aspects) is defaultdict
        assert type(aspectsDetectOnlyTestBear.aspects['detect']) is AspectList
        assert type(aspectsDetectOnlyTestBear.aspects['fix']) is AspectList
        assert aspectsDetectOnlyTestBear.aspects['fix'] == []
        assert (aspectsDetectOnlyTestBear.aspects['detect'] ==
                [CommitMessage.Shortlog.ColonExistence])
        assert (CommitMessage.Shortlog.ColonExistence in
                aspectsDetectOnlyTestBear.aspects['detect'])

    def test_no_detect_aspects(self):
        assert type(aspectsFixOnlyTestBear.aspects) is defaultdict
        assert type(aspectsFixOnlyTestBear.aspects['detect']) is AspectList
        assert type(aspectsFixOnlyTestBear.aspects['fix']) is AspectList
        assert aspectsFixOnlyTestBear.aspects['detect'] == []
        assert (aspectsFixOnlyTestBear.aspects['fix'] ==
                [CommitMessage.Shortlog.TrailingPeriod])
        assert (CommitMessage.Shortlog.TrailingPeriod in
                aspectsFixOnlyTestBear.aspects['fix'])

    def test_detect_and_fix_aspects(self):
        assert type(aspectsTestBear.aspects) is defaultdict
        assert type(aspectsTestBear.aspects['detect']) is AspectList
        assert type(aspectsTestBear.aspects['fix']) is AspectList
        assert aspectsTestBear.aspects == {
            'detect': [CommitMessage.Shortlog.ColonExistence],
            'fix': [CommitMessage.Shortlog.TrailingPeriod],
        }
        assert (CommitMessage.Shortlog.ColonExistence in
                aspectsTestBear.aspects['detect'])
        assert (CommitMessage.Shortlog.TrailingPeriod in
                aspectsTestBear.aspects['fix'])

    def test_simple_api(self):
        self.assertRaises(TypeError, TestBear, self.settings, 2)
        self.assertRaises(TypeError, TestBear, None, self.queue)
        self.assertRaises(NotImplementedError, Bear.kind)

        base = Bear(self.settings, None)
        self.assertRaises(NotImplementedError, base.run)
        self.assertEqual(base.get_non_optional_settings(), {})

    def test_message_queue(self):
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG,
                           'Running bear TestBear...')
        self.check_message(LOG_LEVEL.DEBUG, 'set=up')
        self.check_message(LOG_LEVEL.ERROR, 'teardown')

    def test_bad_bear(self):
        self.uut = BadTestBear(self.settings, self.queue)
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.ERROR,
                           'Bear BadTestBear failed to run. Take a look at '
                           'debug messages (`-V`) for further '
                           'information.')
        # debug message contains custom content, dont test this here
        self.queue.get()

    def test_print_filename_LocalBear(self):
        self.uut = LocalBear(self.settings, self.queue)
        self.uut.execute('filename.py', 'file\n')
        self.check_message(LOG_LEVEL.DEBUG)
        # Fails because of no run() implementation
        self.check_message(LOG_LEVEL.ERROR,
                           'Bear LocalBear failed to run on file filename.py. '
                           'Take a look at debug messages (`-V`) for further '
                           'information.')

    def test_print_no_filename_GlobalBear(self):
        self.uut = GlobalBear(None, self.settings, self.queue)
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        # Fails because of no run() implementation
        self.check_message(LOG_LEVEL.ERROR,
                           'Bear GlobalBear failed to run. Take a look at '
                           'debug messages (`-V`) for further '
                           'information.')

    def test_zero_line_offset_LocalBear(self):
        error_message = 'Line offset cannot be zero.'
        self.uut = ZeroOffsetLocalBear(self.settings,
                                       self.queue,
                                       error_message)
        self.uut.execute('filename.py', 'file\n')
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.ERROR,
                           'Bear ZeroOffsetLocalBear violated one-based '
                           'offset convention.', error_message)

    def test_zero_column_offset_LocalBear(self):
        error_message = 'Column offset cannot be zero.'
        self.uut = ZeroOffsetLocalBear(self.settings,
                                       self.queue,
                                       error_message)
        self.uut.execute('filename.py', 'file\n')
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.ERROR,
                           'Bear ZeroOffsetLocalBear violated one-based '
                           'offset convention.', error_message)

    def test_zero_line_and_column_offset_LocalBear(self):
        error_message = 'Line and column offset cannot be zero.'
        self.uut = ZeroOffsetLocalBear(self.settings,
                                       self.queue,
                                       error_message)
        self.uut.execute('filename.py', 'file\n')
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.ERROR,
                           'Bear ZeroOffsetLocalBear violated one-based '
                           'offset convention.', error_message)

    def test_zero_line_offset_GlobalBear(self):
        error_message = 'Line offset cannot be zero.'
        self.uut = ZeroOffsetGlobalBear(self.settings,
                                        self.queue,
                                        error_message)
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.ERROR,
                           'Bear ZeroOffsetGlobalBear violated one-based '
                           'offset convention.', error_message)

    def test_zero_column_offset_GlobalBear(self):
        error_message = 'Column offset cannot be zero.'
        self.uut = ZeroOffsetGlobalBear(self.settings,
                                        self.queue,
                                        error_message)
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.ERROR,
                           'Bear ZeroOffsetGlobalBear violated one-based '
                           'offset convention.', error_message)

    def test_zero_line_and_column_offset_GlobalBear(self):
        error_message = 'Line and column offset cannot be zero.'
        self.uut = ZeroOffsetGlobalBear(self.settings,
                                        self.queue,
                                        error_message)
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.ERROR,
                           'Bear ZeroOffsetGlobalBear violated one-based '
                           'offset convention.', error_message)

    def test_inconvertible(self):
        self.uut = TypedTestBear(self.settings, self.queue)
        self.settings.append(Setting('something', '5'))
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.assertTrue(self.uut.was_executed)

        self.settings.append(Setting('something', 'nonsense'))
        self.uut.was_executed = False
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.check_message(LOG_LEVEL.WARNING)
        self.assertTrue(self.queue.empty())
        self.assertFalse(self.uut.was_executed)

    def check_message(self, log_level, message=None, regex=False):
        msg = self.queue.get()
        self.assertIsInstance(msg, LogMessage)
        if message:
            if regex:
                self.assertRegexpMatches(msg.message, message)
            else:
                self.assertEqual(msg.message, message)

        self.assertEqual(msg.log_level, log_level, msg)

    def test_no_queue(self):
        uut = TestBear(self.settings, None)
        uut.execute()  # No exceptions

    def test_dependencies(self):
        self.assertEqual(Bear.BEAR_DEPS, set())
        self.assertEqual(Bear.missing_dependencies([]), set())
        self.assertEqual(Bear.missing_dependencies([BadTestBear]), set())

        self.assertEqual(TestBear.missing_dependencies([]), {BadTestBear})
        self.assertEqual(TestBear.missing_dependencies([BadTestBear]), set())
        self.assertEqual(TestBear.missing_dependencies([TestBear]),
                         {BadTestBear})
        self.assertEqual(TestBear.missing_dependencies([TestBear,
                                                        BadTestBear]),
                         set())

    def test_check_prerequisites(self):
        uut = BearWithPrerequisites(self.settings, self.queue, True)
        uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        self.assertTrue(self.queue.empty())
        self.assertTrue(uut.was_executed)

        self.assertRaisesRegex(RuntimeError,
                               'The bear BearWithPrerequisites does not '
                               'fulfill all requirements\\.',
                               BearWithPrerequisites,
                               self.settings,
                               self.queue,
                               False)

        self.check_message(LOG_LEVEL.ERROR,
                           'The bear BearWithPrerequisites does not fulfill '
                           'all requirements.')
        self.assertTrue(self.queue.empty())

        self.assertRaisesRegex(RuntimeError,
                               'The bear BearWithPrerequisites does not '
                               'fulfill all requirements\\. Just because '
                               'I want to\\.',
                               BearWithPrerequisites,
                               self.settings,
                               self.queue,
                               'Just because I want to.')

        self.check_message(LOG_LEVEL.ERROR,
                           'The bear BearWithPrerequisites does not fulfill '
                           'all requirements. Just because I want to.')
        self.assertTrue(self.queue.empty())

    def test_get_non_optional_settings(self):
        self.assertEqual(StandAloneBear.get_non_optional_settings(recurse=True),
                         {'x': ('First value.', int),
                          'y': ('Second value.', int)})

        # Test settings of dependency bears. Also test settings-override-
        # behaviour for dependency bears with equal setting names.
        self.assertEqual(DependentBear.get_non_optional_settings(recurse=True),
                         {'x': ('First value.', int),
                          'y': ('Second value, but better.', int),
                          'w': ('Fourth value.', float)})

        self.assertEqual(DependentBear.get_non_optional_settings(recurse=False),
                         {'y': ('Second value, but better.', int),
                          'w': ('Fourth value.', float)})

    def test_no_warning_debug_enabled_LocalBear(self):
        self.settings.append(Setting('log_level', 'DEBUG'))
        self.uut = LocalBear(self.settings, self.queue)
        self.uut.execute('filename.py', 'file\n')
        self.check_message(LOG_LEVEL.DEBUG, 'Running bear LocalBear...')
        # Fails because of no run() implementation
        self.check_message(LOG_LEVEL.DEBUG,
                           'The bear LocalBear raised an exception. If you '
                           'are the author of this bear, please make sure to '
                           'catch all exceptions. If not and this error '
                           'annoys you, you might want to get in contact with '
                           'the author of this bear.\n\nTraceback information '
                           'is provided below:', True)
        self.assertRaises(NotImplementedError)

    def test_no_warning_debug_enabled_GlobalBear(self):
        self.settings.append(Setting('log_level', 'DEBUG'))
        self.uut = GlobalBear(None, self.settings, self.queue)
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG, 'Running bear GlobalBear...')
        # Fails because of no run() implementation
        self.check_message(LOG_LEVEL.DEBUG,
                           'The bear GlobalBear raised an exception. If you '
                           'are the author of this bear, please make sure to '
                           'catch all exceptions. If not and this error '
                           'annoys you, you might want to get in contact with '
                           'the author of this bear.\n\nTraceback information '
                           'is provided below:', True)
        self.assertRaises(NotImplementedError)

    def test_get_config_dir(self):
        section = Section('default')
        section.append(Setting('files', '**', '/path/to/dir/config'))
        uut = TestBear(section, None)
        self.assertEqual(uut.get_config_dir(), abspath('/path/to/dir'))

    def test_new_result(self):
        bear = Bear(self.settings, None)
        result = bear.new_result('test message', '/tmp/testy')
        expected = Result.from_values(bear, 'test message', '/tmp/testy')
        self.assertEqual(result, expected)

    def test_bear_with_default_language(self):
        self.uut = BearWithLanguage(self.settings, self.queue)
        result = self.uut.execute()[0]
        self.assertIsInstance(result, Language)
        self.assertEqual(str(result), 'Python 3.4')
        self.check_message(LOG_LEVEL.DEBUG)

    def test_bear_with_specific_language(self):
        self.uut = BearWithLanguage(self.settings, self.queue)
        # This should be ignored
        self.settings['language'] = 'Java'
        # Use this instead
        self.settings.language = Language['HTML 5.1']
        result = self.uut.execute()[0]
        self.assertIsInstance(result, Language)
        self.assertEqual(str(result), 'Hypertext Markup Language 5.1')
        self.check_message(LOG_LEVEL.DEBUG)

    # Mock test added to solve the coverage problem by DebugBearsTest
    @patch('pdb.Pdb.do_continue')
    def test_custom_continue(self, do_continue):
        section = Section('name')
        section.append(Setting('debug_bears', 'True'))
        bear = Bear(section, self.queue)
        args = ()
        self.assertEqual(Debugger(bear).do_quit(args), 1)
        pdb.Pdb.do_continue.assert_called_once_with(args)

    # side_effect effectively implements run() method of bear
    @patch('coalib.bears.Bear.Debugger.runcall', side_effect=((1, 2), 1, 2))
    def test_debug_run_with_return(self, runcall):
        section = Section('name')
        section.append(Setting('debug_bears', 'True'))
        my_bear = Bear(section, self.queue)
        args = ()
        kwargs = {}
        self.assertEqual(my_bear.run_bear_from_section(args, kwargs), [1, 2])

    @patch('coalib.bears.Bear.Debugger.runcall', return_value=None)
    def test_debug_run_with_no_return(self, runcall):
        section = Section('name')
        section.append(Setting('debug_bears', 'True'))
        my_bear = Bear(section, self.queue)
        args = ()
        kwargs = {}
        self.assertIsNone(my_bear.run_bear_from_section(args, kwargs))

    def test_do_settings(self):
        section = Section('name', None)
        section.append(Setting('x', '85'))
        section.append(Setting('y', 'kbc3'))
        section.append(Setting('z', '75'))
        bear = TestOneBear(section, self.queue)
        output = StringIO()
        dbg = Debugger(bear, stdout=output)
        arg = ()
        self.assertEqual(dbg.do_settings(arg), 1)
        output = output.getvalue().splitlines()
        self.assertEqual(output[0], 'x = 85')
        self.assertEqual(output[1], "y = 'kbc3'")
        self.assertEqual(output[2], 'z = 75')
        self.assertEqual(output[3], "w = 'kbc'")
        with self.assertRaises(ValueError):
            Debugger(bear=None)

    def test_is_debugged(self):
        with self.assertRaises(ValueError):
            _is_debugged(bear=None)

        section = Section('name')
        uut = Bear(section, self.queue)
        self.assertEqual(_is_debugged(uut), False)
        section.append(Setting('debug_bears', 'tRuE'))
        self.assertEqual(_is_debugged(uut), True)
        section.append(Setting('debug_bears', '0'))
        self.assertEqual(_is_debugged(uut), False)
        section.append(Setting('debug_bears', 'Bear, ABear'))
        self.assertEqual(_is_debugged(uut), True)
        section.append(Setting('debug_bears', 'abc, xyz'))
        self.assertEqual(_is_debugged(uut), False)

    @patch('cProfile.Profile.dump_stats')
    def test_profiler_with_no_directory_exists(self, dump_stats):
        args = ()
        kwargs = {}
        section = Section('name')
        section.append(Setting('profile', 'tRuE'))
        bear = TestTwoBear(section, self.queue)
        self.assertEqual(bear.run_bear_from_section(args, kwargs), [1, 2, 3])
        dump_stats.assert_called_once_with(join(os.getcwd(),
                                                'name_TestTwoBear.prof'))
        section.append(Setting('profile', 'abc'))
        bear = TestTwoBear(section, self.queue)
        self.assertEqual(bear.run_bear_from_section(args, kwargs), [1, 2, 3])
        dump_stats.assert_called_with(os.path.join(
            bear.profile, 'name_TestTwoBear.prof'))
        os.rmdir('abc')
        section.append(Setting('profile', '1'))
        bear = TestThreeBear(section, self.queue)
        self.assertIsNone(bear.run_bear_from_section(args, kwargs))
        dump_stats.assert_called_with(join(os.getcwd(),
                                           'name_TestThreeBear.prof'))

    @patch('cProfile.Profile.dump_stats')
    def test_profiler_with_directory_exists(self, dump_stats):
        args = ()
        kwargs = {}
        section = Section('name')
        with TemporaryDirectory() as temp_dir:
            section.append(Setting('profile', temp_dir))
            bear = TestTwoBear(section, self.queue)
            self.assertEqual(bear.run_bear_from_section(args, kwargs),
                             [1, 2, 3])
            dump_stats.assert_called_once_with(os.path.join(
                bear.profile, 'name_TestTwoBear.prof'))

    def test_profiler_with_file_path(self):
        args = ()
        kwargs = {}
        section = Section('name')
        with NamedTemporaryFile() as temp_file:
            section.append(Setting('profile', temp_file.name))
            bear = TestTwoBear(section, self.queue)
            with self.assertRaises(SystemExit) as context:
                bear.run_bear_from_section(args, kwargs)
                self.assertEqual(context.exception.code, 2)

    def test_profiler_with_debugger(self):
        section = Section('name')
        section.append(Setting('debug_bears', 'tRuE'))
        section.append(Setting('profile', 'tRuE'))
        with self.assertRaisesRegex(
                ValueError,
                'Cannot run debugger and profiler at the same time.'):
            Bear(section, self.queue)

    @patch('coalib.bears.Bear.Bear.profile_run')
    def test_profiler_with_false_setting(self, profile_run):
        args = ()
        kwargs = {}
        section = Section('name')
        section.append(Setting('profile', '0'))
        bear = TestThreeBear(section, self.queue)
        self.assertIsNone(bear.run_bear_from_section(args, kwargs))
        assert not profile_run.called

    def test_is_profiled(self):
        with self.assertRaisesRegex(
                ValueError,
                'Positional argument bear is not an instance of Bear class.'):
            _is_profiled(bear=None)

        section = Section('name')
        uut = Bear(section, self.queue)
        self.assertEqual(_is_profiled(uut), False)
        section.append(Setting('profile', 'tRuE'))
        self.assertEqual(_is_profiled(uut), os.getcwd())
        section.append(Setting('profile', '0'))
        self.assertEqual(_is_profiled(uut), False)
        section.append(Setting('profile', 'dirpath'))
        self.assertEqual(_is_profiled(uut), 'dirpath')

    def test_setting_is_enabled(self):
        with self.assertRaisesRegex(
                ValueError,
                'Positional argument bear is not an instance of Bear class.'):
            _setting_is_enabled(bear=None, key='key')

        section = Section('name')
        uut = Bear(section, self.queue)
        with self.assertRaisesRegex(ValueError, 'No setting key passed.'):
            _setting_is_enabled(bear=uut, key=None)

        self.assertFalse(_setting_is_enabled(bear=uut, key='key'))

        section.append(Setting('key', 'value'))
        self.assertEqual(_setting_is_enabled(bear=uut, key='key'),
                         uut.section['key'])
        section.append(Setting('key', 'tRuE'))
        self.assertEqual(_setting_is_enabled(bear=uut, key='key'), True)
        section.append(Setting('key', '0'))
        self.assertEqual(_setting_is_enabled(bear=uut, key='key'), False)

    def test_profiler_dependency(self, debug=False):
        with bear_test_module():
            with prepare_file(['#fixme  '], None) as (lines, filename):
                results = run_coala(console_printer=ConsolePrinter(),
                                    log_printer=LogPrinter(),
                                    arg_list=(
                                        '-c', os.devnull,
                                        '-f', filename,
                                        '-b', 'DependentBear',
                                        '-S', 'use_spaces=yeah',
                                        '--profile', 'profiled_bears',
                                    ),
                                    autoapply=False,
                                    debug=debug)
                cli_result = results[0]['cli']
                self.assertEqual(len(cli_result), 1)

        profiled_files = os.listdir('profiled_bears')
        self.assertEqual(len(profiled_files), 1)
        self.assertEqual(profiled_files[0], 'cli_SpaceConsistencyTestBear.prof')
        shutil.rmtree('profiled_bears')


class BrokenReadHTTPResponse(BytesIO):

    def __init__(self, chunks, *args, **kwargs):
        self.read_count = 0
        self.chunks = chunks

    def read(self, *args, **kwargs):
        # A HTTPResponse will return an empty string when you read from it
        # after the socket has been closed.
        if self.closed:
            return b''

        if self.read_count == len(self.chunks):
            raise requests.exceptions.ReadTimeout('Fake read timeout')

        self.read_count += 1
        return self.chunks[self.read_count - 1]


class BearDownloadTest(BearTestBase):

    def setUp(self):
        super().setUp()
        self.mock_url = 'https://test.com'
        self.filename = 'test.html'
        self.teapot_url = 'https://www.google.com/teapot'
        # 'https://httpstat.us/418' and
        # http://httpbin.org/status/418 also work
        self.file_location = join(self.uut.data_dir, self.filename)

    def test_connection_timeout_mocked(self):
        exc = requests.exceptions.ConnectTimeout
        with requests_mock.Mocker() as reqmock:
            reqmock.get(self.mock_url, exc=exc)
            with self.assertRaisesRegex(exc, '^$'):
                self.uut.download_cached_file(
                    self.mock_url, self.filename)

    def test_read_broken(self):
        exc = (
            requests.exceptions.RequestException,
        )
        fake_content = [b'Fake read data', b'Another line']
        fake_content_provider = BrokenReadHTTPResponse(fake_content)

        self.assertFalse(isfile(self.file_location))

        with requests_mock.Mocker() as reqmock:
            reqmock.get(self.mock_url, body=fake_content_provider)
            with self.assertRaisesRegex(exc, 'Fake read timeout'):
                self.uut.download_cached_file(
                    self.mock_url, self.filename)

        self.assertTrue(isfile(self.file_location))

        with open(self.file_location, 'rb') as fh:
            self.assertEqual(fh.read(), b''.join(fake_content))

    def test_status_code_error(self):
        exc = requests.exceptions.HTTPError
        with self.assertRaisesRegex(exc, '^418 '):
            self.uut.download_cached_file(
                self.teapot_url, self.filename)

    def test_download_cached_file(self):
        mock_url = 'https://test.com'
        mock_text = """<html>
            <p> lorem impsum dolor</p>
        </html>"""
        filename = self.filename
        file_location = self.file_location

        with freeze_time('2017-01-01') as frozen_datetime:
            with requests_mock.Mocker() as reqmock:

                reqmock.get(mock_url, text=mock_text)
                self.assertFalse(isfile(file_location))
                expected_filename = file_location
                result_filename = self.uut.download_cached_file(mock_url,
                                                                filename)
                self.assertTrue(isfile(join(file_location)))
                self.assertEqual(result_filename, expected_filename)
                expected_time = getmtime(file_location)

                frozen_datetime.tick(delta=datetime.timedelta(seconds=0.5))
                result_filename = self.uut.download_cached_file(mock_url,
                                                                filename)
                self.assertEqual(result_filename, expected_filename)
                result_time = getmtime(file_location)
                self.assertEqual(result_time, expected_time)
