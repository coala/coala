import platform
import subprocess
import unittest
from unittest.mock import patch

try:
    import distro
except subprocess.CalledProcessError:
    pass

from coalib.bears.requirements.DistributionRequirement import (
    DistributionRequirement)


@unittest.skipIf(platform.system() == 'Windows',
                 "This test cannot be run on Windows.")
class DistributionRequirementTestCase(unittest.TestCase):

    @patch('distro.linux_distribution', return_value=('Fedora',))
    def test_install_command_mock_fedora(self, call_mock):
        self.assertEqual(distro.linux_distribution()[0], 'Fedora')
        self.assertEqual(DistributionRequirement(
            dnf='libclang', apt_get='libclangs').install_command(),
            ['dnf', 'install', 'libclang'])

    @patch('distro.linux_distribution', return_value=('bad_os',))
    def test_install_command_mock_incompatible_os(self, call_mock):
        self.assertEqual(distro.linux_distribution()[0], 'bad_os')
        with self.assertRaises(OSError):
            DistributionRequirement(
                dnf='libclang', apt_get='libclangs').install_command()
