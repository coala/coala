import unittest
import shutil
from coalib.bears.requirements.NpmRequirement import NpmRequirement


class NpmRequirementTestCase(unittest.TestCase):

    @unittest.skipIf(shutil.which('npm') is None, "Npm is not installed.")
    def test_InstalledRequirement(self):
        self.assertTrue(NpmRequirement('npm').is_installed())

    @unittest.skipIf(shutil.which('npm') is None, "Npm is not installed.")
    def test_NotInstalledRequirement(self):
        self.assertFalse(NpmRequirement('some_bad_package').is_installed())
