import unittest
import sys
import shelve
import os


sys.path.insert(0, ".")
from coalib.output.gui.support.ProjectMetadata import ProjectMetadata


class ProjectMetadataTest(unittest.TestCase):
    def test_add_project(self):
        projectMetadata = ProjectMetadata()
        projectMetadata.add_project("Key", "Test")
        shelf = shelve.open(projectMetadata.file)
        self.assertTrue("Key" in shelf)
        shelf.close()
        projectMetadata.delete_project("Key")
        shelf = shelve.open(projectMetadata.file)
        self.assertTrue("Key" not in shelf)
        shelf.close()
        os.remove(projectMetadata.file)


if __name__ == '__main__':
    unittest.main(verbosity=2)
