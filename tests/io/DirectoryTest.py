import os
import unittest

from coalib.io.Directory import Directory


class DirectoryTest(unittest.TestCase):

    def setUp(self):
        self.test_dir_path = os.path.join(os.path.dirname(__file__),
                                          'DirectoryTestDir')
        self.another_test_dir_path = os.path.join(os.path.dirname(__file__),
                                                  'DirectoryTestDir', 'Dir1')
        self.uut = Directory(self.test_dir_path)

    def test_equal(self):
        self.assertEqual(self.uut, Directory(self.test_dir_path))
        self.assertNotEqual(self.uut, Directory(self.another_test_dir_path))

    def test_get_children(self):
        self.assertEqual(len(self.uut.get_children()), 3)

    def test_get_children_recursively(self):
        self.assertEqual(len(self.uut.get_children_recursively()), 5)

    def test_path(self):
        self.assertEqual(self.uut.path, self.test_dir_path)

    def test_parent(self):
        self.assertEqual(self.uut.parent, os.path.dirname(self.test_dir_path))

    def test_timestamp(self):
        self.assertEqual(self.uut.timestamp,
                         os.path.getmtime(self.test_dir_path))
