import unittest
import shutil
import sys
from coalib.bears.requirements.PipRequirement import PipRequirement


@unittest.skipIf(shutil.which('pip') is None, "Pip is not installed.")
class PipRequirementTestCase(unittest.TestCase):

    def test_install_command_with_version(self):
        self.assertEqual(
            [sys.executable, '-m', 'pip', 'install', 'setuptools==19.2'],
            PipRequirement('setuptools', '19.2').install_command())

    def test_install_command_without_version(self):
        self.assertEqual([sys.executable, '-m', 'pip', 'install', 'setuptools'],
                         PipRequirement('setuptools').install_command())

    def test_installed_requirement(self):
        self.assertTrue(PipRequirement('pip').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(PipRequirement('some_bad_package').is_installed())
