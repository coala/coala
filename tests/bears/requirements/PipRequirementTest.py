import unittest
import shutil
from coalib.bears.requirements.PipRequirement import PipRequirement


class PipRequirementTestCase(unittest.TestCase):

    @unittest.skipIf(shutil.which('pip') is None, "Pip is not installed.")
    def test_InstalledRequirement(self):
        self.assertTrue(PipRequirement('pip').is_installed())

    @unittest.skipIf(shutil.which('pip') is None, "Pip is not installed.")
    def test_NotInstalledRequirement(self):
        self.assertFalse(PipRequirement('some_bad_package').is_installed())
