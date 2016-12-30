import unittest
import shutil
from coalib.bears.requirements.CabalRequirement import CabalRequirement


@unittest.skipIf(shutil.which('cabal') is None, 'Cabal is not installed.')
class CabalRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(CabalRequirement('cabal').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(CabalRequirement('some_bad_package').is_installed())
