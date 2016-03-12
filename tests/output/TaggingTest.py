import os
import unittest

from pyprint.NullPrinter import NullPrinter

from coalib.output.printers.LogPrinter import LogPrinter
from coalib.output.Tagging import (
    delete_tagged_results, get_tag_path, load_tagged_results, tag_results)


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
        path = get_tag_path("test_tag_create", "test_path", self.log_printer)
        try:
            tag_results("test_tag_create", "test_path", {}, self.log_printer)
            results = load_tagged_results("test_tag_create",
                                          "test_path",
                                          self.log_printer)
            self.assertEqual(results, {})
        finally:
            delete_tagged_results("test_tag_create",
                                  "test_path",
                                  self.log_printer)

        none_path = get_tag_path("None", "test_path", self.log_printer)
        tag_results("None", "test_path", {}, self.log_printer)
        self.assertFalse(os.path.exists(none_path))
        results = load_tagged_results("None", "test_path", self.log_printer)
        self.assertEquals(results, None)

    def test_delete_tagged_results_no_file(self):
        path = get_tag_path("test_tag_del", "test_path", self.log_printer)
        none_path = get_tag_path("None", "test_path", self.log_printer)
        open(path, "a").close()
        open(none_path, "a").close()
        delete_tagged_results("None", "test_path", self.log_printer)
        self.assertTrue(os.path.exists(none_path))

        delete_tagged_results("test_tag_del", "test_path", self.log_printer)
        self.assertFalse(os.path.exists(path))

        delete_tagged_results("test_tag_del2", "test_path", self.log_printer)
        self.assertFalse(os.path.exists(path))

        os.remove(none_path)

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
