from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import call_without_output
import platform


class GemRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``ruby`` packages automatically and provide a function to check
    for the requirement.
    """

    def __init__(self, package, version='', require=''):
        """
        Constructs a new ``GemRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = GemRequirement('setuptools', '19.2', 'flag')
        >>> pr.type
        'gem'
        >>> pr.package
        'setuptools'
        >>> pr.version
        '19.2'
        >>> pr.require
        'flag'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        :param require: A string that specifies any additional flags, that
                        would be used with ``require``.
        """
        PackageRequirement.__init__(self, 'gem', package, version)
        self.require = require

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        cmd = ['gem', 'list', '-i', self.package]
        if platform.system() == 'Windows':  # pragma: no cover
            cmd = ['cmd', '/c'] + cmd
        return not call_without_output(cmd)
