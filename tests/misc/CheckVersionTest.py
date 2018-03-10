import unittest

from coalib.misc.CheckVersion import check_version
from pkg_resources import get_distribution


class CheckVersionTest(unittest.TestCase):

    def test_check_version(self):
        test_package = 'package'
        bad_version = '0'
        self.assertFalse(check_version(test_package, bad_version))
        test_package = 'pip'
        good_version = get_distribution(test_package).version
        self.assertTrue(check_version(test_package, good_version))
        self.assertFalse(check_version(test_package, bad_version))
