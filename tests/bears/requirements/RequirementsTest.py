import unittest
import shutil
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.bears.requirements.NpmRequirement import NpmRequirement
from coalib.bears.requirements.GemRequirement import GemRequirement


class PipRequirementTestCase(unittest.TestCase):

    def setUp(self):
        self.PipRequirement = PipRequirement('pip')
        self.PipRequirementBad = PipRequirement('some_bad_package')

    @unittest.skipIf(shutil.which('pip') is None, "Pip is not installed.")
    def test_InstalledRequirement(self):
        self.assertEqual(self.PipRequirement.is_installed(), True)

    @unittest.skipIf(shutil.which('pip') is None, "Pip is not installed.")
    def test_NotInstalledRequirement(self):
        self.assertEqual(self.PipRequirementBad.is_installed(), False)


class NpmRequirementTestCase(unittest.TestCase):

    def setUp(self):
        self.NpmRequirement = NpmRequirement('npm')
        self.NpmRequirementBad = PipRequirement('some_bad_package')

    @unittest.skipIf(shutil.which('npm') is None, "Npm is not installed.")
    def test_InstalledRequirement(self):
        self.assertEqual(self.NpmRequirement.is_installed(), True)

    @unittest.skipIf(shutil.which('npm') is None, "Npm is not installed.")
    def test_NotInstalledRequirement(self):
        self.assertEqual(self.NpmRequirementBad.is_installed(), False)


class GemRequirementTestCase(unittest.TestCase):

    def setUp(self):
        self.GemRequirement = GemRequirement('ruby')
        self.GemRequirementBad = PipRequirement('some_bad_package')

    @unittest.skipIf(shutil.which('gem') is None, "Ruby is not installed.")
    def test_InstalledRequirement(self):
        self.assertEqual(self.GemRequirement.is_installed(), True)

    @unittest.skipIf(shutil.which('gem') is None, "Ruby is not installed.")
    def test_NotInstalledRequirement(self):
        self.assertEqual(self.GemRequirementBad.is_installed(), False)
