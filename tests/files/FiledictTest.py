import unittest
import queue
import os

from coalib.files.Filedict import get_file_dict
from coalib.output.printers.LogPrinter import LogPrinter


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

    def test_get_file_dict(self):
        file_dict = get_file_dict([self.testcode_c_path], self.log_printer)
        self.assertEqual(len(file_dict), 1)
        self.assertEqual(
            "Files that will be checked:\n" + self.testcode_c_path,
            self.log_printer.log_queue.get().message)

    def test_get_file_dict_non_existent_file(self):
        file_dict = get_file_dict(["non_existent_file"], self.log_printer)
        self.assertEqual(file_dict, {})
        self.assertIn(("Failed to read file 'non_existent_file' because of "
                       "an unknown error."),
                      self.log_printer.log_queue.get().message)