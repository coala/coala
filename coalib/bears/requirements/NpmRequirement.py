from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import call_without_output
import platform


class NpmRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``npm``, without using the manager name.
    """

    def __init__(self, package, version=""):
        """
        Constructs a new ``NpmRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = NpmRequirement('ramllint', '6.2')
        >>> pr.manager
        'npm'
        >>> pr.package
        'ramllint'
        >>> pr.version
        '6.2'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'npm', package, version)

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> NpmRequirement('alex', '2').install_command()
        'npm install alex@2'

        >>> NpmRequirement('alex').install_command()
        'npm install alex'

        :param return: A string with the installation command.
        """
        if self.version:
            return "npm install {}@{}".format(self.package, self.version)
        return "npm install {}".format(self.package)

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        cmd = ['npm', 'show', self.package]
        if platform.system() == 'Windows':
            cmd = ['cmd', '/c'] + cmd
        return not call_without_output(cmd)
