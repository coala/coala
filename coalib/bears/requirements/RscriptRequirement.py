from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import run_shell_command


class RscriptRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``, and helps specifying
    requirements from ``R``, without using the manager name.
    """

    def __init__(self, package, version="", flag="", repo=""):
        """
        Constructs a new ``RscriptRequirement``, using the
        ``PackageRequirement`` constructor.

        >>> pr = RscriptRequirement(
        ...         'formatR', version='1.4', flag='-e',
        ...         repo="http://cran.rstudio.com")
        >>> pr.manager
        'R'
        >>> pr.package
        'formatR'
        >>> pr.version
        '1.4'
        >>> pr.flag
        '-e'
        >>> pr.repo
        'http://cran.rstudio.com'

        :param package: A string with the name of the package to be installed.
        :param version: A version string. Leave empty to specify latest version.
        :param flag:    A string that specifies any additional flags, that
                        are passed to the manager.
        :param repo:    The repository from which the package to be installed is
                        from.
        """
        PackageRequirement.__init__(self, 'R', package, version)
        self.flag = flag
        self.repo = repo

    def install_command(self):
        """
        Creates the installation command for the instance of the class.

        >>> RscriptRequirement(
        ...     'formatR', '' , '-e',
        ...     'http://cran.rstudio.com').install_command()
        'R -e "install.packages(\"formatR\", repo=\"http://cran.rstudio.com\", dependencies=TRUE)"'

        :param return: A string with the installation command.
        """
        return ('R {} "install.packages(\"{}\", repo=\"{}\", '
                'dependencies=TRUE)"'.format(self.flag,
                                             self.package, self.repo))

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        return True if run_shell_command(
                ('R -e \'library(\"{}\", quietly=TRUE)\''
                 .format(self.package)))[1] is '' else False
