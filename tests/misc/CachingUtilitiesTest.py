import os
import unittest

from pyprint.NullPrinter import NullPrinter

from coalib.misc.CachingUtilities import (
    get_settings_hash, settings_changed, update_settings_db,
    get_data_path, pickle_load, pickle_dump, delete_files)
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.settings.Section import Section


class CachingUtilitiesTest(unittest.TestCase):

    def setUp(self):
        self.log_printer = LogPrinter(NullPrinter())

    def test_corrupt_cache_files(self):
        file_path = get_data_path(self.log_printer, 'corrupt_file')
        with open(file_path, 'wb') as f:
            f.write(bytes([1] * 100))

        self.assertTrue(os.path.isfile(file_path))
        self.assertEqual(pickle_load(
            self.log_printer, 'corrupt_file', fallback=42), 42)

    def test_delete_files(self):
        pickle_dump(self.log_printer, 'coala_test', {'answer': 42})
        self.assertTrue(delete_files(
            self.log_printer, ['coala_test']))
        self.assertFalse(os.path.isfile(get_data_path(
            self.log_printer, 'coala_test')))

    def test_delete_invalid_file(self):
        self.assertFalse(delete_files(
            self.log_printer, ['non_existant_file']))

    @unittest.mock.patch('coalib.misc.CachingUtilities.os')
    def test_delete_permission_error(self, mock_os):
        with open(get_data_path(self.log_printer, 'coala_test'), 'w'):
            mock_os.remove.side_effect = OSError('Permission error')
            self.assertTrue(os.path.isfile(get_data_path(
                self.log_printer, 'coala_test')))
            self.assertFalse(delete_files(self.log_printer, ['coala_test']))

    @unittest.mock.patch('os.makedirs')
    def test_permission_error(self, makedirs):
        makedirs.side_effect = PermissionError
        self.assertEqual(get_data_path(self.log_printer, 'test'), None)

        self.assertFalse(pickle_dump(self.log_printer, 'test', {'answer': 42}))


class SettingsTest(unittest.TestCase):

    def setUp(self):
        self.log_printer = LogPrinter(NullPrinter())

    def test_settings_change(self):
        sections = {}
        settings_hash = get_settings_hash(sections)
        update_settings_db(self.log_printer, settings_hash)
        self.assertFalse(settings_changed(self.log_printer, settings_hash))

        sections = {'a': Section('a')}
        settings_hash = get_settings_hash(sections)
        self.assertTrue(settings_changed(self.log_printer, settings_hash))

    def test_targets_change(self):
        sections = {'a': Section('a'), 'b': Section('b')}
        self.assertNotEqual(get_settings_hash(sections),
                            get_settings_hash(sections, targets=['a']))
