import unittest
from setuptools.dist import Distribution
from distutils.errors import DistutilsOptionError

from coalib.output.dbus.BuildDbusService import BuildDbusService
from coalib.misc import Constants
from coalib.misc.ContextManagers import make_temp


class BuildDbusServiceTest(unittest.TestCase):

    def test_build(self):
        dist = Distribution()
        uut = BuildDbusService(dist)
        self.assertRaises(DistutilsOptionError, uut.finalize_options)
        with make_temp() as uut.output:
            uut.finalize_options()

            uut.run()
            with open(uut.output) as file:
                result = file.read(1000)

            self.assertEqual(
                result,
                "[D-BUS Service]\nNames=" + Constants.BUS_NAME +
                "\nExec=coala-dbus")


if __name__ == "__main__":
    unittest.main(verbosity=2)
