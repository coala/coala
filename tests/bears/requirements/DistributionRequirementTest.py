import platform
import unittest
from unittest.mock import patch

from coalib.bears.requirements.DistributionRequirement import (
    DistributionRequirement)


class DistributionRequirementTestCase(unittest.TestCase):

    @patch('platform.linux_distribution', return_value=('Fedora',))
    def test_install_command_mock_fedora(self, call_mock):
        self.assertEqual(platform.linux_distribution()[0], 'Fedora')
        self.assertEqual(DistributionRequirement(
            dnf='libclang', apt_get='libclangs').install_command(),
            'dnf install libclang')

    @patch('platform.linux_distribution', return_value=('bad_os',))
    def test_install_command_mock_incompatible_os(self, call_mock):
        self.assertEqual(platform.linux_distribution()[0], 'bad_os')
        with self.assertRaises(OSError):
            DistributionRequirement(
                dnf='libclang', apt_get='libclangs').install_command()
