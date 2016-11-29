import multiprocessing
from os import remove
from os.path import abspath, exists, getmtime, isfile, join
import requests_mock
import shutil
from time import sleep
import unittest

from coalib.bears.Bear import Bear
from coalib.results.Result import Result
from coalib.output.printers.LOG_LEVEL import LOG_LEVEL
from coalib.processes.communication.LogMessage import LogMessage
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class BadTestBear(Bear):

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

    def run(self):
        raise NotImplementedError


class TestBear(Bear):

    BEAR_DEPS = {BadTestBear}

    def __init__(self, section, queue):
        Bear.__init__(self, section, queue)

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


class BearTest(unittest.TestCase):

    def setUp(self):
        self.queue = multiprocessing.Queue()
        self.settings = Section('test_settings')
        self.uut = TestBear(self.settings, self.queue)

    def tearDown(self):
        if exists(self.uut.data_dir):
            shutil.rmtree(self.uut.data_dir)

    def test_simple_api(self):
        self.assertRaises(TypeError, TestBear, self.settings, 2)
        self.assertRaises(TypeError, TestBear, None, self.queue)
        self.assertRaises(NotImplementedError, self.uut.kind)

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

    @requests_mock.Mocker()
    def assert_downcache(self, uut, mock_url,  # test download caching
                         mock_headers, filename, mock_req):
        """
        All tests here are mocked and don't connect to the Internet.
        This method checks that the bear really is caching its
        requirements when the etag or last modified date are the same
        as remote
        """
        test_html = '''<html>
            <p> help</p>
        </html>'''
        mock_req.head(mock_url, headers=mock_headers, status_code=200)
        mock_req.get(mock_url, text=test_html,
                     headers=mock_headers, status_code=200)

        expected_file = join(uut.data_dir, filename)
        self.assertFalse(isfile(expected_file))
        result_file = uut.download_cached_file(mock_url, filename)
        self.assertTrue(isfile(expected_file))
        self.assertEqual(result_file, expected_file)
        expected_time = getmtime(expected_file)
        sleep(0.5)  # needed to make sure there is a second between downloads
        result_file = uut.download_cached_file(mock_url, filename)
        self.assertTrue(isfile(expected_file))
        self.assertEqual(result_file, expected_file)
        result_time = getmtime(expected_file)
        self.assertEqual(result_time, expected_time)
        shutil.rmtree(uut.data_dir)

    @requests_mock.Mocker()
    def assert_down_nocache(self, uut, mock_url,  # test download caching
                            mock_old_headers, mock_new_headers,
                            filename, mock_req):
        """
        All tests here are mocked and don't connect to the Internet.
        This method checks that the bear really is downloading its
        requirements when the etag or last modified date goes out of sync
        """
        test_html = '''<html>
            <p> help</p>
        </html>'''
        mock_req.head(mock_url, headers=mock_old_headers, status_code=200)
        mock_req.get(mock_url, text=test_html,
                     headers=mock_old_headers, status_code=200)

        expected_file = join(uut.data_dir, filename)
        self.assertFalse(isfile(expected_file))
        result_file = uut.download_cached_file(mock_url, filename)
        self.assertTrue(isfile(expected_file))
        self.assertEqual(result_file, expected_file)
        expected_time = getmtime(expected_file)

        sleep(0.5)  # needed to make sure there is a second between downloads
        mock_req.head(mock_url, headers=mock_new_headers, status_code=200)
        mock_req.get(mock_url, text=test_html,
                     headers=mock_new_headers, status_code=200)
        result_file = uut.download_cached_file(mock_url, filename)
        self.assertTrue(isfile(expected_file))
        self.assertEqual(result_file, expected_file)
        result_time = getmtime(expected_file)
        self.assertNotEqual(result_time, expected_time)
        shutil.rmtree(uut.data_dir)

    def test_download_cached_file(self):
        etag = {'etag': 'a334000-53803c616e5c0'}
        new_etag = {'etag': 'b355400-53803c616e5c0'}
        last_modified = {'last-modified': 'Tue, 19 Jul 2016 21:29:03 GMT'}
        new_modified = {'last-modified': 'Mon, 15 Aug 2016 09:15:55 GMT'}

        self.assert_downcache(self.uut, 'http://etag.com', etag,
                              'downfile.html')
        self.assert_downcache(self.uut, 'http://lastmodified.com',
                              last_modified, 'downfile.html')
        self.assert_down_nocache(self.uut, 'http://etag.com', etag, new_etag,
                                 'redown.html')
        self.assert_down_nocache(self.uut, 'http://modified.com',
                                 last_modified, new_modified, 'redown.html')
        self.assert_down_nocache(self.uut, 'http://noheader.com', {}, {},
                                 'redown.html')

    @requests_mock.Mocker()
    def test_download_cached_file_edgecase(self, mock_req):
        """
        Test the edge-case where the user deletes the actual file, but forgets
        to remove the version tracker file
        """
        filename = 'noversion.html'
        test_html = '''<html>
            <p> help</p>
        </html>'''
        mock_req.head('http://edgecase.com', status_code=200)
        mock_req.get('http://edgecase.com', text=test_html, status_code=200)

        self.assertFalse(isfile(join(self.uut.data_dir, filename)))
        self.uut.download_cached_file('http://edgecase.com', filename)
        self.assertTrue(isfile(join(self.uut.data_dir, filename)))
        expected_time = getmtime(join(self.uut.data_dir, filename))
        remove(join(self.uut.data_dir, filename))
        sleep(0.5)  # needed to make sure there is a second between downloads
        self.uut.download_cached_file('http://edgecase.com', filename)
        result_time = getmtime(join(self.uut.data_dir, filename))
        self.assertNotEqual(result_time, expected_time)
