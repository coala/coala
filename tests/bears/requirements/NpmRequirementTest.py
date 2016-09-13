import unittest
import unittest.mock
import shutil
from coalib.bears.requirements.NpmRequirement import NpmRequirement


@unittest.skipIf(shutil.which('npm') is None, "Npm is not installed.")
class NpmRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        with unittest.mock.patch(
                'coalib.bears.requirements.NpmRequirement.call_without_output',
                return_value=0):
            self.assertTrue(NpmRequirement('some_good_package').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(NpmRequirement('some_bad_package').is_installed())
