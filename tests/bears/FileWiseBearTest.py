import unittest

from coalib.bears.FileWiseBear import BEAR_KIND, FileWiseBear
from coalib.settings.Section import Section


class DummyFileProxy:

    def __init__(self, lines):
        self.lines = lines


class FileWiseBearTest(unittest.TestCase):

    def setUp(self):
        file_set = {DummyFileProxy([]), DummyFileProxy(["a\n"])}
        self.test_object = FileWiseBear(file_set, Section("Name"), None)

    def test_api(self):
        test_object = FileWiseBear(None, Section("name"), None)
        self.assertRaises(NotImplementedError,
                          test_object.analyze,
                          "file")

    def test_kind(self):
        self.assertEqual(FileWiseBear.kind(), BEAR_KIND.FILEWISE)

    def test_bear_executions(self):
        for task in self.test_object.generate_tasks():
            self.assertRaises(NotImplementedError,
                              self.test_object.execute_task,
                              task[0],
                              task[1])
