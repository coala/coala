from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import call_without_output


class GoRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``go``, without using the manager name.
    """

    def __init__(self, package, version="", flag=""):
        """
        Constructs a new ``GoRequirement``, using the ``PackageRequirement``
        constructor.

        >>> pr = GoRequirement('github.com/golang/lint/golint', '19.2', '-u')
        >>> pr.manager
        'go'
        >>> pr.package
        'github.com/golang/lint/golint'
        >>> pr.version
        '19.2'
        >>> pr.flag
        '-u'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        :param flag:    A string that specifies any additional flags, that
                        are passed to the manager.
        """
        PackageRequirement.__init__(self, 'go', package, version)
        self.flag = flag

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> GoRequirement(
        ...     'github.com/golang/lint/golint', '' , '-u' ).install_command()
        ['go', 'get', '-u', 'github.com/golang/lint/golint']

        :param return: A string with the installation command.
        """
        return ['go', 'get', self.flag, self.package]

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        return not call_without_output(('go', 'list', self.package))
