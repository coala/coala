import shutil
import unittest
from coalib.bears.requirements.RscriptRequirement import RscriptRequirement
from coalib.misc.Shell import call_without_output


@unittest.skipIf(shutil.which('R') is None, 'R is not installed.')
class RscriptRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(RscriptRequirement('base').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(RscriptRequirement('some_bad_package').is_installed())
