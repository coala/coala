import unittest
import shutil
from coalib.bears.requirements.NpmRequirement import NpmRequirement


@unittest.skipIf(shutil.which('npm') is None, "Npm is not installed.")
class NpmRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(NpmRequirement('npm').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(NpmRequirement('some_bad_package').is_installed())
