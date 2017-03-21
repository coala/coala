from collections import defaultdict
from io import BytesIO
import multiprocessing
import unittest
from os.path import abspath, exists, isfile, join, getmtime
import shutil
from time import sleep

import requests
import requests_mock

from coalib.bearlib.aspects.Metadata import CommitMessage
from coalib.bears.Bear import Bear
from coalib.bears.BEAR_KIND import BEAR_KIND
from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.processes.communication.LogMessage import LogMessage
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


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


class TypedTestBear(Bear):

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)
        self.was_executed = False

    def run(self, something: int):
        self.was_executed = True
        return []


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

    def run(self, x: int, y: int, z: int=33):
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
}):
    pass


class aspectsDetectOnlyTestBear(Bear, aspects={
        'detect': [CommitMessage.Shortlog.ColonExistence],
}):
    pass


class aspectsFixOnlyTestBear(Bear, aspects={
        'fix': [CommitMessage.Shortlog.TrailingPeriod],
}):
    pass


class BearTestBase(unittest.TestCase):

    def setUp(self):
        self.queue = multiprocessing.Queue()
        self.settings = Section('test_settings')
        self.uut = TestBear(self.settings, self.queue)

    def tearDown(self):
        if exists(self.uut.data_dir):
            shutil.rmtree(self.uut.data_dir)


class BearTest(BearTestBase):

    def test_default_aspects(self):
        assert type(Bear.aspects) is defaultdict
        assert Bear.aspects['detect'] == Bear.aspects['fix'] == []

    def test_no_fix_aspects(self):
        assert type(aspectsDetectOnlyTestBear.aspects) is defaultdict
        assert aspectsDetectOnlyTestBear.aspects['fix'] == []
        assert (aspectsDetectOnlyTestBear.aspects['detect'] ==
                [CommitMessage.Shortlog.ColonExistence])

    def test_no_detect_aspects(self):
        assert type(aspectsFixOnlyTestBear.aspects) is defaultdict
        assert aspectsFixOnlyTestBear.aspects['detect'] == []
        assert (aspectsFixOnlyTestBear.aspects['fix'] ==
                [CommitMessage.Shortlog.TrailingPeriod])

    def test_detect_and_fix_aspects(self):
        assert type(aspectsTestBear.aspects) is defaultdict
        assert aspectsTestBear.aspects == {
            'detect': [CommitMessage.Shortlog.ColonExistence],
            'fix': [CommitMessage.Shortlog.TrailingPeriod],
        }

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
        self.check_message(LOG_LEVEL.WARNING,
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
        self.check_message(LOG_LEVEL.WARNING,
                           'Bear LocalBear failed to run on file filename.py. '
                           'Take a look at debug messages (`-V`) for further '
                           'information.')

    def test_print_no_filename_GlobalBear(self):
        self.uut = GlobalBear(None, self.settings, self.queue)
        self.uut.execute()
        self.check_message(LOG_LEVEL.DEBUG)
        # Fails because of no run() implementation
        self.check_message(LOG_LEVEL.WARNING,
                           'Bear GlobalBear failed to run. Take a look at '
                           'debug messages (`-V`) for further '
                           'information.')

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

    def check_message(self, log_level, message=None):
        msg = self.queue.get()
        self.assertIsInstance(msg, LogMessage)
        if message:
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
        self.file_location = join(self.uut.data_dir, self.filename)

    def test_connection_timeout_mocked(self):
        exc = requests.exceptions.ConnectTimeout
        with requests_mock.Mocker() as reqmock:
            reqmock.get(self.mock_url, exc=exc)
            with self.assertRaisesRegexp(exc, '^$'):
                self.uut.download_cached_file(
                    self.mock_url, self.filename)

    def test_read_broken(self):
        exc = requests.exceptions.RequestException
        fake_content = [b'Fake read data', b'Another line']
        fake_content_provider = BrokenReadHTTPResponse(fake_content)

        self.assertFalse(isfile(self.file_location))

        with requests_mock.Mocker() as reqmock:
            reqmock.get(self.mock_url, body=fake_content_provider)
            with self.assertRaisesRegexp(exc, 'Fake read timeout'):
                self.uut.download_cached_file(
                    self.mock_url, self.filename)

        self.assertTrue(isfile(self.file_location))
        self.assertEqual(open(self.file_location, 'rb').read(),
                         b''.join(fake_content))

    def test_status_code_error(self):
        exc = requests.exceptions.HTTPError
        with self.assertRaisesRegexp(exc, '418 Client Error'):
            self.uut.download_cached_file(
                'http://httpbin.org/status/418', self.filename)

    def test_download_cached_file(self):
        mock_url = 'https://test.com'
        mock_text = """<html>
            <p> lorem impsum dolor</p>
        </html>"""
        filename = self.filename
        file_location = self.file_location

        with requests_mock.Mocker() as reqmock:
            reqmock.get(mock_url, text=mock_text)
            self.assertFalse(isfile(file_location))
            expected_filename = file_location
            result_filename = self.uut.download_cached_file(mock_url, filename)
            self.assertTrue(isfile(join(file_location)))
            self.assertEqual(result_filename, expected_filename)
            expected_time = getmtime(file_location)
            sleep(0.5)

            result_filename = self.uut.download_cached_file(mock_url, filename)
            self.assertEqual(result_filename, expected_filename)
            result_time = getmtime(file_location)
            self.assertEqual(result_time, expected_time)
