import os
import unittest

from coalib.output.Tagging import (
    delete_tagged_results, get_tag_path, load_tagged_results, tag_results)


class TaggingTest(unittest.TestCase):

    def test_get_tag_path(self):
        self.assertEqual(get_tag_path("a", "b"), get_tag_path("a", "b"))
        self.assertNotEqual(get_tag_path("a", "b"), get_tag_path("a", "c"))
        self.assertNotEqual(get_tag_path("a", "b"), get_tag_path("c", "b"))

    def test_tag_results(self):
        try:
            tag_results("test_tag", "test_path", {})
            results = load_tagged_results("test_tag", "test_path")
            self.assertEqual(results, {})
        finally:
            delete_tagged_results("test_tag", "test_path")

    def test_delete_tagged_results_no_file(self):
        delete_tagged_results("test_tag", "test_path")
        self.assertFalse(os.path.exists(get_tag_path("test_tag", "test_path")))
