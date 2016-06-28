import shutil
import unittest
from coalib.bears.requirements.GemRequirement import GemRequirement


class GemRequirementTestCase(unittest.TestCase):

    @unittest.skipIf(shutil.which('gem') is None, "Gem is not installed.")
    def test_InstalledRequirement(self):
        self.assertTrue(GemRequirement('gem').is_installed())

    @unittest.skipIf(shutil.which('gem') is None, "Gem is not installed.")
    def test_NotInstalledRequirement(self):
        self.assertFalse(GemRequirement('some_bad_package').is_installed())
