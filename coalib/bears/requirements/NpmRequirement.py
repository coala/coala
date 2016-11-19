from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import call_without_output
import platform


class NpmRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``npm`` packages automatically and provide a function to check
    for the requirement.
    """

    def __init__(self, package, version=''):
        """
        Constructs a new ``NpmRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = NpmRequirement('ramllint', '6.2')
        >>> pr.type
        'npm'
        >>> pr.package
        'ramllint'
        >>> pr.version
        '6.2'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        """
        PackageRequirement.__init__(self, 'npm', package, version)

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        for cmd in (['npm', 'list', self.package],
                    ['npm', 'list', '-g', self.package]):

            if platform.system() == 'Windows':  # pragma: no cover
                cmd = ['cmd', '/c'] + cmd

            if not call_without_output(cmd):
                return True

        return False
