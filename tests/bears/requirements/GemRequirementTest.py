import shutil
import unittest
from coalib.bears.requirements.GemRequirement import GemRequirement


@unittest.skipIf(shutil.which('gem') is None, "Gem is not installed.")
class GemRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(GemRequirement('gem').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(GemRequirement('some_bad_package').is_installed())
