import unittest
import shutil
from coalib.bears.requirements.PipRequirement import PipRequirement


@unittest.skipIf(shutil.which('pip') is None, "Pip is not installed.")
class PipRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(PipRequirement('pip').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(PipRequirement('some_bad_package').is_installed())
