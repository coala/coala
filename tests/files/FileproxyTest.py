import unittest
import os

from coalib.files.Fileproxy import Fileproxy


class FileproxyTest(unittest.TestCase):

    def setUp(self):
        fileproxy_test_dir = os.path.join(os.path.split(__file__)[0],
                                          'FileproxyTestFiles')

        self.testfile = os.path.join(fileproxy_test_dir, 'testfile.txt')
        self.fileproxyobject = Fileproxy(self.testfile)

    def test_equal(self):
        self.assertEqual(self.fileproxyobject, Fileproxy(self.testfile))

    def test_iter(self):
        with open(self.testfile, 'r') as file:
            self.assertEqual(tuple(self.fileproxyobject),
                             tuple(file.readlines()))

    def test_hashing(self):
        self.assertEqual(hash(self.fileproxyobject),
                         hash(Fileproxy(self.testfile)))
