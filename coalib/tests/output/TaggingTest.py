import os
from pyprint.NullPrinter import NullPrinter
import unittest

from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.Tagging import (get_tag_path,
                                   tag_results,
                                   load_tagged_results,
                                   delete_tagged_results)


def raise_permission_error(*args, **kwargs):
    raise PermissionError


class TaggingTest(unittest.TestCase):

    def setUp(self):
        self.log_printer = LogPrinter(NullPrinter())

    def test_get_tag_path(self):
        self.assertEqual(get_tag_path("a", "b", self.log_printer),
                         get_tag_path("a", "b", self.log_printer))
        self.assertNotEqual(get_tag_path("a", "b", self.log_printer),
                            get_tag_path("a", "c", self.log_printer))
        self.assertNotEqual(get_tag_path("a", "b", self.log_printer),
                            get_tag_path("c", "b", self.log_printer))

    def test_tag_results(self):
        try:
            tag_results("test_tag", "test_path", {}, self.log_printer)
            results = load_tagged_results("test_tag",
                                          "test_path",
                                          self.log_printer)
            self.assertEqual(results, {})
        finally:
            delete_tagged_results("test_tag", "test_path", self.log_printer)

    def test_delete_tagged_results_no_file(self):
        delete_tagged_results("test_tag", "test_path", self.log_printer)
        self.assertFalse(os.path.exists(get_tag_path("test_tag",
                                                     "test_path",
                                                     self.log_printer)))

    def test_permission_error(self):
        old_makedirs = os.makedirs
        os.makedirs = raise_permission_error

        self.assertEqual(get_tag_path("a", "b", self.log_printer), None)
        tag_results("test_tag", "test_path", {}, self.log_printer)
        results = load_tagged_results("test_tag",
                                      "test_path",
                                      self.log_printer)
        self.assertEqual(results, None)

        os.makedirs = old_makedirs
