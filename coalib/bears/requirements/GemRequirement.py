from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import call_without_output
import platform


class GemRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``gem``, without using the manager name.
    """

    def __init__(self, package, version="", require=""):
        """
        Constructs a new ``GemRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = GemRequirement('setuptools', '19.2', 'flag')
        >>> pr.manager
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

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> GemRequirement('rubocop').install_command()
        ['gem', 'install', 'rubocop']

        >>> GemRequirement('scss_lint', '', 'false').install_command()
        ['gem', 'install', 'scss_lint, require: false']

        :param return: A string with the installation command.
        """
        result = ['gem', 'install', self.package + ', require: ' + self.require
                  if self.require else self.package]
        return result

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        cmd = ['gem', 'list', '-i', self.package]
        if platform.system() == 'Windows':  # pragma: no cover
            cmd = ['cmd', '/c'] + cmd
        return not call_without_output(cmd)
