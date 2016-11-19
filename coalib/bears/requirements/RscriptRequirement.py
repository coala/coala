from coalib.bears.requirements.PackageRequirement import PackageRequirement
from coalib.misc.Shell import run_shell_command


class RscriptRequirement(PackageRequirement):
    """
    This class is a subclass of ``PackageRequirement``. It specifies the proper
    type for ``R`` packages automatically and provide a function to check
    for the requirement.
    """

    def __init__(self, package, version='', flag='', repo=''):
        """
        Constructs a new ``RscriptRequirement``, using the
        ``PackageRequirement`` constructor.

        >>> pr = RscriptRequirement(
        ...         'formatR', version='1.4', flag='-e',
        ...         repo="http://cran.rstudio.com")
        >>> pr.type
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
                        are passed to the type.
        :param repo:    The repository from which the package to be installed is
                        from.
        """
        PackageRequirement.__init__(self, 'R', package, version)
        self.flag = flag
        self.repo = repo

    def is_installed(self):
        """
        Checks if the dependency is installed.

        :param return: True if dependency is installed, false otherwise.
        """
        return True if run_shell_command(
                ('R -e \'library(\"{}\", quietly=TRUE)\''
                 .format(self.package)))[1] is '' else False
