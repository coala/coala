import sys
import unittest
import tempfile
import os
from setuptools.dist import Distribution
from distutils.errors import DistutilsOptionError

sys.path.insert(0, ".")
from coalib.output.dbus.BuildDbusService import BuildDbusService
from coalib.misc import Constants


class BuildDbusServiceTest(unittest.TestCase):

    def test_build(self):
        dist = Distribution()
        uut = BuildDbusService(dist)
        self.assertRaises(DistutilsOptionError, uut.finalize_options)
        handle, uut.output = tempfile.mkstemp(text=True)

        uut.finalize_options()

        uut.run()
        result = os.read(handle, 1000).decode()

        self.assertEqual(
            result,
            "[D-BUS Service]\nNames=" + Constants.BUS_NAME +
            "\nExec=coala-dbus")


if __name__ == "__main__":
    unittest.main(verbosity=2)
