import unittest
import shutil
from coalib.bears.requirements.GoRequirement import GoRequirement


@unittest.skipIf(shutil.which('go') is None, "Go is not installed.")
class GoRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(GoRequirement('fmt').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(GoRequirement('some_bad_package').is_installed())
