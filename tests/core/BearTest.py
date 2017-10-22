import datetime
from itertools import permutations
from os.path import abspath, exists, isfile, join, getmtime
import shutil
import unittest

from dependency_management.requirements.PipRequirement import PipRequirement

from freezegun import freeze_time

import requests

import requests_mock

from coalib.core.Bear import Bear
from coalib.results.Result import Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class Bear1(Bear):
    pass


class Bear2(Bear):
    pass


class BearWithAnalysis(Bear):

    def analyze(self, x: int, y: int, z: int=33):
        """
        Analyzes stuff.

        :param x: First value.
        :param y: Second value.
        :param z: Third value.
        """
        yield x
        yield y
        yield z


class BearWithMoreAnalysis(Bear):
    BEAR_DEPS = {BearWithAnalysis}

    def analyze(self, y: int, w: float):
        """
        Analyzes even more stuff.

        :param y: Second value, but better.
        :param w: Fourth value.
        """
        yield y
        yield w


class BearWithPrerequisites(Bear):
    REQUIREMENTS = {PipRequirement('super-super-bad-package'),
                    PipRequirement('even-even-worse-package')}


class BearWithPrerequisitesOverride(Bear):
    prerequisites_fulfilled = True

    @classmethod
    def check_prerequisites(cls):
        return cls.prerequisites_fulfilled


class BearTest(unittest.TestCase):

    def tearDown(self):
        defined_bears = [
            value
            for value in globals().values()
            if isinstance(value, type) and issubclass(value, Bear)]

        for bear in defined_bears:
            if exists(bear.data_dir):
                shutil.rmtree(bear.data_dir)

    def test_invalid_types_at_instantiation(self):
        with self.assertRaises(TypeError):
            Bear(Section('test-section'), 2)

        with self.assertRaises(TypeError):
            Bear(None, {})

    def test_analyze(self):
        with self.assertRaises(NotImplementedError):
            Bear(Section('test-section'), {}).analyze()

    def test_generate_tasks(self):
        with self.assertRaises(NotImplementedError):
            Bear(Section('test-section'), {}).generate_tasks()

    def test_execute_task(self):
        # Test the default implementation of execute_task().
        section = Section('test-section')
        filedict = {}

        uut = BearWithAnalysis(section, filedict)

        results = uut.execute_task((10, 20), {'z': 30})

        self.assertEqual(results, [10, 20, 30])

    def test_check_prerequisites(self):
        section = Section('test-section')
        filedict = {}

        # Test default implementation.
        expected_possibilities = [
            'Following requirements are not installed: '
            '{} (installable via `{}`), {} (installable via `{}`)'.format(
                req1.package, ' '.join(req1.install_command()),
                req2.package, ' '.join(req2.install_command()))
            for req1, req2 in permutations(BearWithPrerequisites.REQUIREMENTS)
        ]

        self.assertIn(BearWithPrerequisites.check_prerequisites(),
                      expected_possibilities)

        # Test correct exception throwing in constructor.
        BearWithPrerequisitesOverride.prerequisites_fulfilled = True
        BearWithPrerequisitesOverride(section, filedict)

        BearWithPrerequisitesOverride.prerequisites_fulfilled = False
        with self.assertRaises(RuntimeError) as cm:
            BearWithPrerequisitesOverride(section, filedict)

        self.assertEqual(
            str(cm.exception),
            'The bear BearWithPrerequisitesOverride does not fulfill all '
            'requirements.')

        BearWithPrerequisitesOverride.prerequisites_fulfilled = (
            'This is on purpose due to running inside a test.')
        with self.assertRaises(RuntimeError) as cm:
            BearWithPrerequisitesOverride(section, filedict)

        self.assertEqual(
            str(cm.exception),
            'The bear BearWithPrerequisitesOverride does not fulfill all '
            'requirements. This is on purpose due to running inside a test.')

    def test_get_metadata(self):
        uut = BearWithAnalysis.get_metadata()
        self.assertEqual(uut.non_optional_params,
                         {'x': ('First value.', int),
                          'y': ('Second value.', int)})
        self.assertEqual(
            uut.optional_params,
            {'z': ("Third value. (Optional, defaults to '33'.)", int, 33)})

    def test_get_non_optional_settings(self):
        self.assertEqual(BearWithAnalysis.get_non_optional_settings(),
                         {'x': ('First value.', int),
                          'y': ('Second value.', int)})

        # Test settings of dependency bears. Also test settings-override-
        # behaviour for dependency bears with equal setting names.
        self.assertEqual(BearWithMoreAnalysis.get_non_optional_settings(),
                         {'x': ('First value.', int),
                          'y': ('Second value, but better.', int),
                          'w': ('Fourth value.', float)})

    def test_new_result(self):
        bear = Bear(Section('test-section'), {})
        result = bear.new_result('test message', '/tmp/testy')
        expected = Result.from_values(bear, 'test message', '/tmp/testy')
        self.assertEqual(result, expected)

    def test_get_config_dir(self):
        section = Section('default')
        section.append(Setting('files', '**', '/path/to/dir/config'))
        uut = Bear(section, {})
        self.assertEqual(uut.get_config_dir(), abspath('/path/to/dir'))

    def test_download_cached_file(self):
        section = Section('default')
        uut = Bear(section, {})

        mock_url = 'https://test.com'
        mock_text = """<html>
            <p> lorem ipsum dolor</p>
        </html>"""
        filename = 'test.html'
        file_location = join(uut.data_dir, filename)

        with freeze_time('2017-01-01') as frozen_datetime, \
                requests_mock.Mocker() as reqmock:

            reqmock.get(mock_url, text=mock_text)
            self.assertFalse(isfile(file_location))
            expected_filename = file_location
            result_filename = uut.download_cached_file(mock_url, filename)
            self.assertTrue(isfile(join(file_location)))
            self.assertEqual(result_filename, expected_filename)
            expected_time = getmtime(file_location)

            frozen_datetime.tick(delta=datetime.timedelta(seconds=0.5))
            result_filename = uut.download_cached_file(mock_url, filename)
            self.assertEqual(result_filename, expected_filename)
            result_time = getmtime(file_location)
            self.assertEqual(result_time, expected_time)

    def test_download_cached_file_connection_timeout_mocked(self):
        mock_url = 'https://test.com'
        exc = requests.exceptions.ConnectTimeout
        with requests_mock.Mocker() as reqmock:
            reqmock.get(mock_url, exc=exc)
            with self.assertRaisesRegex(exc, '^$'):
                Bear.download_cached_file(
                    mock_url, 'test.html')

    def test_download_cached_file_status_code_error(self):
        exc = requests.exceptions.HTTPError
        with self.assertRaisesRegex(exc, '418 Client Error'):
            Bear.download_cached_file(
                'http://httpbin.org/status/418', 'test.html')

    def test_json(self):
        result = BearWithAnalysis.__json__()

        # data_dir and source_location are system dependent, so remove them for
        # further tests.
        self.assertIn('data_dir', result)
        del result['data_dir']
        del result['source_location']

        expected = {
            'ASCIINEMA_URL': '',
            'AUTHORS': set(),
            'AUTHORS_EMAILS': set(),
            'BEAR_DEPS': set(),
            'CAN_DETECT': set(),
            'CAN_FIX': set(),
            'INCLUDE_LOCAL_FILES': set(),
            'LANGUAGES': set(),
            'LICENSE': '',
            'MAINTAINERS': set(),
            'MAINTAINERS_EMAILS': set(),
            'metadata': {
                'desc': 'Analyzes stuff.',
                'non_optional_params': {
                    'x': 'First value.',
                    'y': 'Second value.'},
                'optional_params': {
                    'z': "Third value. (Optional, defaults to '33'.)"}},
            'name': 'BearWithAnalysis',
            'PLATFORMS': {'any'},
            'REQUIREMENTS': set()}

        self.assertEqual(result, expected)
