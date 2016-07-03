import unittest
import shutil
from coalib.bears.requirements.JuliaRequirement import JuliaRequirement


@unittest.skipIf(shutil.which('julia') is None, "Julia is not installed.")
class JuliaRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(JuliaRequirement("Lint", '', '-e').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(JuliaRequirement(
            "some_bad_package", '', '-e').is_installed())
