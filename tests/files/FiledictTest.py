import unittest
import queue
import os

from coalib.files.Filedict import get_file_dict
from coalib.output.printers.LogPrinter import LogPrinter
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.misc.Caching import FileCache


class FiledictTestLogPrinter(LogPrinter):

    def __init__(self, log_queue):
        LogPrinter.__init__(self, self)
        self.log_queue = log_queue
        self.set_up = False

    def log_message(self, log_message, timestamp=None, **kwargs):
        self.log_queue.put(log_message)


class FiledictTest(unittest.TestCase):

    def setUp(self):
        self.log_queue = queue.Queue()
        self.log_printer = FiledictTestLogPrinter(self.log_queue)

        self.testcode_c_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "FiledictTestFiles",
            "testcode.c"))

        self.test_section = Section("test", None)
        self.test_section.append(Setting("files", self.testcode_c_path))

    def test_get_file_dict(self):
        complete_file_dict, file_dict = get_file_dict(self.test_section,
                                                      None,
                                                      self.log_printer)
        self.assertEqual(len(complete_file_dict), 1)
        self.assertEqual(
            "Files that will be checked:\n" + self.testcode_c_path,
            self.log_printer.log_queue.get().message)

    def test_get_file_dict_cache(self):
        cache = FileCache(FiledictTestLogPrinter(queue.Queue()),
                          "coala_test",
                          flush_cache=True)
        complete_file_dict, file_dict = get_file_dict(self.test_section,
                                                      cache,
                                                      self.log_printer)
        self.assertEqual(len(file_dict), 1)
        cache.write()
        complete_file_dict, file_dict = get_file_dict(self.test_section,
                                                      cache,
                                                      self.log_printer)

        self.assertEqual(len(file_dict), 0)

    def test_get_file_dict_non_existent_file(self):
        no_file_sec = Section("test", None)
        no_file_sec.append(Setting("files", "no_file"))
        complete_file_dict, file_dict = get_file_dict(no_file_sec,
                                                      None,
                                                      self.log_printer)
        self.assertEqual(complete_file_dict, {})
        self.assertEqual(file_dict, {})
        self.assertIn(("No files matching '"+os.getcwd()+"/no_file' were "
                                                         "found."),
                      self.log_printer.log_queue.get().message)
