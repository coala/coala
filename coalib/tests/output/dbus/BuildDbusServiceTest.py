import sys
import unittest
import tempfile
from setuptools.dist import Distribution
from distutils.errors import DistutilsOptionError

sys.path.insert(0, ".")
from coalib.output.dbus.BuildDbusService import BuildDbusService
from coalib.misc.Constants import Constants


class BuildDbusServiceTest(unittest.TestCase):
    def test_build(self):
        dist = Distribution()
        uut = BuildDbusService(dist)
        self.assertRaises(DistutilsOptionError, uut.finalize_options)
        uut.output = tempfile.mkstemp()[1]

        uut.finalize_options()

        uut.run()
        result = open(uut.output).read()

        self.assertEqual(
            result,
            "[D-BUS Service]\nNames=" + Constants.BUS_NAME +
            "\nExec=coala-dbus")


if __name__ == "__main__":
    unittest.main(verbosity=2)
