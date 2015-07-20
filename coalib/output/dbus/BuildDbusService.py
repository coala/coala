from distutils.core import Command
from distutils.errors import DistutilsOptionError

from coalib.misc.Constants import Constants


class BuildDbusService(Command):
    """
    Add a `build_dbus` command  to your setup.py.
    To use this Command class add a command to call this class::

        # For setuptools
        setup(
              entry_points={
                "distutils.commands": [
                    "build_dbus = coalib.misc.BuildDbusService:BuildDbusService"
                ]
              }
        )

        # For distutils
        from coalib.misc.BuildDbusService import BuildDbusService
        setup(
              cmdclass={'build_dbus': BuildDbusService}
        )

    You can then use the following setup command to produce a dbus service::

        $ python setup.py build_dbus
    """
    user_options = [('output=', 'O', 'output file')]

    def initialize_options(self):
        self.output = None

    def finalize_options(self):
        if self.output is None:
            raise DistutilsOptionError('\'output\' option is required')
        self.announce('Writing dbus service %s' % self.output)

    def run(self):
        dist = self.distribution
        dbus_service = ("[D-BUS Service]\n"
                        "Names=" + Constants.BUS_NAME + "\n"
                        "Exec=coala-dbus")

        with open(self.output, 'w') as f:
            f.write(dbus_service)

