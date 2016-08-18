import unittest

from coalib.bears.ProjectWideBear import BEAR_KIND, ProjectWideBear
from coalib.settings.Section import Section


class DummyFileProxy:

    def __init__(self, lines):
        self.lines = lines


class ProjectWideBearTest(unittest.TestCase):

    def setUp(self):
        file_set = {DummyFileProxy([]), DummyFileProxy(["a\n"])}
        self.test_object = ProjectWideBear(file_set, Section("Name"), None)

    def test_api(self):
        test_object = ProjectWideBear(None, Section("name"), None)
        self.assertRaises(NotImplementedError,
                          test_object.analyze,
                          {})

    def test_kind(self):
        self.assertEqual(ProjectWideBear.kind(), BEAR_KIND.PROJECTWIDE)

    def test_bear_executions(self):
        task = self.test_object.generate_tasks()
        self.assertRaises(NotImplementedError,
                          self.test_object.execute_task,
                          task[0],
                          task[1])
