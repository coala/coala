from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import call_without_output
import sys


class PipRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``pip``, without using the manager name.
    """

    MANAGER = sys.executable + ' -m pip'

    def __init__(self, package, version=""):
        """
        Constructs a new ``PipRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = PipRequirement('setuptools', '19.2')
        >>> pr.manager
        'pip'
        >>> pr.package
        'setuptools'
        >>> pr.version
        '19.2'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'pip', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        :param return: A string with the installation command.
        """
        result = "{} install {}".format(self.MANAGER, self.package)
        if self.version:
            result += "=={}".format(self.version)
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        return not call_without_output(('pip', 'show', self.package))
