import platform
import shutil
import unittest
from coalib.bears.requirements.GemRequirement import GemRequirement
from coalib.misc.Shell import call_without_output

cmd = ['gem', 'list', '-i', 'ruby']
if platform.system() == 'Windows':  # pragma: no cover
    cmd = ['cmd', '/c'] + cmd


@unittest.skipIf(shutil.which('gem') is None or bool(call_without_output(cmd)),
                 "Gem is not installed.")
class GemRequirementTestCase(unittest.TestCase):

    def test_installed_requirement(self):
        self.assertTrue(GemRequirement('ruby').is_installed())

    def test_not_installed_requirement(self):
        self.assertFalse(GemRequirement('some_bad_package').is_installed())
